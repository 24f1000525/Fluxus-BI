import os
import uuid
import tempfile
import pandas as pd
from dotenv import load_dotenv

# Load environment variables for deployment & local usage
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from GroqService import GroqService

app = Flask(__name__)
# Enable CORS for the Vue frontend
CORS(app)

# Local temporary upload directory
UPLOAD_FOLDER = tempfile.gettempdir()
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the LLM Service
groq_service = GroqService()

# In-memory storage for datasets (for demonstration purposes only)
# In production, use a Database and Cloud Storage (e.g. S3)
datasets_db = {}


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "fluxus-bi-backend",
        "status": "ok",
        "message": "Backend is running. Use /upload, /generate-chart, and /query endpoints."
    }), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/upload', methods=['POST'])
def upload_csv():
    """
    Handles CSV upload.
    Uses Pandas to analyze the schema, detect columns, and summarize data distribution.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            schema, df = groq_service.analyze_csv(filepath)
            doc_id = str(uuid.uuid4())
            
            datasets_db[doc_id] = {
                "filepath": filepath,
                "schema": schema,
                "df": df
            }
            
            # --- Auto-Dashboard Generation (Zero-LLM) ---
            numeric_cols = [c for c, t in schema["types"].items() if 'int' in str(t).lower() or 'float' in str(t).lower()]
            cat_cols = [c for c, t in schema["types"].items() if c not in numeric_cols]
            
            auto_charts = []
            
            # --- 1. Metric Cards (KPIs) ---
            auto_charts.append({
                "is_metric": True,
                "title": "Total Records",
                "value": f"{len(df):,}",
                "grid_w": 3, "grid_h": 4
            })
            
            if numeric_cols:
                col1 = numeric_cols[0]
                val1 = df[col1].sum()
                auto_charts.append({
                    "is_metric": True, "title": f"Total {col1}", "value": f"{val1:,.2f}" if isinstance(val1, float) else f"{val1:,}",
                    "grid_w": 3, "grid_h": 4
                })
                
                if len(numeric_cols) > 1:
                    col2 = numeric_cols[1]
                    val2 = df[col2].mean()
                    auto_charts.append({
                        "is_metric": True, "title": f"Avg {col2}", "value": f"{val2:,.2f}",
                        "grid_w": 3, "grid_h": 4
                    })
                else:
                    val2 = df[col1].mean()
                    auto_charts.append({
                        "is_metric": True, "title": f"Avg {col1}", "value": f"{val2:,.2f}",
                        "grid_w": 3, "grid_h": 4
                    })
                    
                if len(numeric_cols) > 2:
                    val3 = df[numeric_cols[2]].max()
                    val_title = f"Max {numeric_cols[2]}"
                else:
                    val3 = df[col1].max()
                    val_title = f"Max {col1}"
                    
                auto_charts.append({
                    "is_metric": True, "title": val_title, "value": f"{val3:,.2f}" if isinstance(val3, float) else f"{val3:,}",
                    "grid_w": 3, "grid_h": 4
                })

            # Title formatting helper
            def format_title(title): return {"text": title, "left": "center", "textStyle": {"fontSize": 14, "fontWeight": "600", "color": "#374151"}}

            if len(cat_cols) > 0 and len(numeric_cols) > 0:
                x_col = cat_cols[0]
                y_col = numeric_cols[0]
                
                # Main wide bar chart (Overview)
                auto_charts.append({
                    "title": format_title(f"{y_col} across {x_col}"),
                    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                    "xAxis": {"type": "category", "axisLabel": {"rotate": 30}},
                    "yAxis": {"type": "value"},
                    "series": [{"type": "bar", "encode": {"x": x_col, "y": y_col}, "itemStyle": {"borderRadius": [4, 4, 0, 0]}}],
                    "grid_w": 8, "grid_h": 12
                })
                
                # Pie Chart
                auto_charts.append({
                    "title": format_title(f"{y_col} Distribution"),
                    "tooltip": {"trigger": "item"},
                    "series": [{"type": "pie", "radius": ["40%", "70%"], "itemStyle": {"borderRadius": 8, "borderColor": "#fff", "borderWidth": 2}, "encode": {"itemName": x_col, "value": y_col}}],
                    "grid_w": 4, "grid_h": 12
                })

                if len(numeric_cols) > 1:
                    y2_col = numeric_cols[1]
                    auto_charts.append({
                        "title": format_title(f"{y2_col} Timeline / Trend"),
                        "tooltip": {"trigger": "axis"},
                        "xAxis": {"type": "category", "boundaryGap": False},
                        "yAxis": {"type": "value"},
                        "series": [{"type": "line", "smooth": True, "encode": {"x": x_col, "y": y2_col}, "areaStyle": {"opacity": 0.2}, "lineStyle": {"width": 3}}],
                        "grid_w": 6, "grid_h": 11
                    })
                    
                    # Donut Chart Variant
                    auto_charts.append({
                        "title": format_title(f"{y2_col} Donut Breakdown"),
                        "tooltip": {"trigger": "item"},
                        "series": [{"type": "pie", "radius": ["55%", "75%"], "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2}, "encode": {"itemName": x_col, "value": y2_col}}],
                        "grid_w": 4, "grid_h": 12
                    })
                    
                    # Horizontal Bar Chart
                    auto_charts.append({
                        "title": format_title(f"Horizontal View: {y2_col}"),
                        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                        "xAxis": {"type": "value"},
                        "yAxis": {"type": "category", "inverse": True},
                        "series": [{"type": "bar", "encode": {"x": y2_col, "y": x_col}, "itemStyle": {"borderRadius": [0, 4, 4, 0]}}],
                        "grid_w": 8, "grid_h": 11
                    })
                    
                    if len(cat_cols) > 1:
                        cat2 = cat_cols[1]
                        auto_charts.append({
                            "title": format_title(f"{y_col} by {cat2}"),
                            "tooltip": {"trigger": "axis"},
                            "xAxis": {"type": "value"},
                            "yAxis": {"type": "category"},
                            "series": [{"type": "bar", "encode": {"x": y_col, "y": cat2}, "itemStyle": {"borderRadius": [0, 4, 4, 0]}}],
                            "grid_w": 6, "grid_h": 11
                        })
                    else:
                        auto_charts.append({
                            "title": format_title(f"{numeric_cols[0]} vs {numeric_cols[1]}"),
                            "tooltip": {"trigger": "item"},
                            "xAxis": {"type": "value", "scale": True},
                            "yAxis": {"type": "value", "scale": True},
                            "series": [{"type": "scatter", "symbolSize": 12, "encode": {"x": numeric_cols[0], "y": numeric_cols[1]}}],
                            "grid_w": 6, "grid_h": 11
                        })

                if len(numeric_cols) > 2:
                    y3_col = numeric_cols[2]
                    # Solid Area Chart
                    auto_charts.append({
                        "title": format_title(f"{y3_col} Volume Area"),
                        "tooltip": {"trigger": "axis"},
                        "xAxis": {"type": "category", "boundaryGap": False},
                        "yAxis": {"type": "value"},
                        "series": [{"type": "line", "smooth": True, "encode": {"x": x_col, "y": y3_col}, "areaStyle": {"opacity": 0.8}, "lineStyle": {"width": 0}}],
                        "grid_w": 6, "grid_h": 11
                    })
                        
            elif len(numeric_cols) > 0:
                y_col = numeric_cols[0]
                auto_charts.append({
                    "title": format_title(f"{y_col} Overview"),
                    "tooltip": {"trigger": "axis"},
                    "xAxis": {"type": "category"},
                    "yAxis": {"type": "value"},
                    "series": [{"type": "bar", "encode": {"y": y_col}, "itemStyle": {"borderRadius": [4, 4, 0, 0]}}],
                    "grid_w": 8, "grid_h": 12
                })
                
                auto_charts.append({
                    "title": format_title(f"{y_col} Trend"),
                    "tooltip": {"trigger": "axis"},
                    "xAxis": {"type": "category"},
                    "yAxis": {"type": "value"},
                    "series": [{"type": "line", "smooth": True, "encode": {"y": y_col}, "areaStyle": {"opacity": 0.3}}],
                    "grid_w": 4, "grid_h": 12
                })

                if len(numeric_cols) > 1:
                    y2_col = numeric_cols[1]
                    auto_charts.append({
                        "title": format_title(f"{y_col} vs {y2_col}"),
                        "tooltip": {"trigger": "item"},
                        "xAxis": {"type": "value", "scale": True},
                        "yAxis": {"type": "value", "scale": True},
                        "series": [{"type": "scatter", "symbolSize": 12, "encode": {"x": y_col, "y": y2_col}}],
                        "grid_w": 6, "grid_h": 12
                    })
                    
                    auto_charts.append({
                        "title": format_title(f"{y2_col} Breakdown"),
                        "tooltip": {"trigger": "item"},
                        "series": [{"type": "pie", "radius": ["40%", "70%"], "encode": {"value": y2_col}}],
                        "grid_w": 6, "grid_h": 12
                    })
            
            import numpy as np
            import re
            
            df_subset = df.head(500).replace({np.nan: None})
            base_name = os.path.splitext(file.filename)[0]
            clean_name = re.sub(r'[-_]', ' ', base_name).title()
            dashboard_title = f"{clean_name} Analysis Dashboard"
            
            return jsonify({
                "message": "File processed successfully",
                "doc_id": doc_id,
                "schema": schema,
                "auto_charts": auto_charts,
                "dataset_subset": df_subset.to_dict(orient="records"),
                "dashboard_title": dashboard_title
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Failed to analyze CSV: {str(e)}"}), 500
            
    return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400


@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    """
    Takes natural language prompt and dataset ID,
    Returns an ECharts JSON configuration via LangChain + Grok.
    """
    data = request.json
    doc_id = data.get('doc_id')
    prompt = data.get('prompt')
    
    if not doc_id or doc_id not in datasets_db:
        return jsonify({"error": "Invalid or missing doc_id"}), 400
        
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400
        
    try:
        import numpy as np
        schema = datasets_db[doc_id]["schema"]
        df = datasets_db[doc_id]["df"]
        chart_config = groq_service.generate_chart_config(prompt, schema)
        
        # Inject the dataset directly into the ECharts JSON config
        # We limit to 500 rows to ensure the browser doesn't freeze with large visualizations
        df_subset = df.head(500).replace({np.nan: None})
        chart_config["dataset"] = {
            "source": df_subset.to_dict(orient="records")
        }
        
        return jsonify({"config": chart_config}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/query', methods=['POST'])
def query_data():
    """
    Data Q&A Bot endpoint. Uses LangChain's Pandas DataFrame agent (or custom LLM logic)
    to answer questions about the specific CSV data.
    """
    data = request.json
    doc_id = data.get('doc_id')
    question = data.get('question')
    
    if not doc_id or doc_id not in datasets_db:
        return jsonify({"error": "Invalid or missing doc_id"}), 400
        
    if not question:
        return jsonify({"error": "Missing question"}), 400
        
    try:
        df = datasets_db[doc_id]["df"]
        answer = groq_service.query_data(question, df)
        return jsonify({"answer": answer}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# In-memory storage for published dashboards
published_dashboards_db = {}

@app.route('/publish', methods=['POST'])
def publish_dashboard():
    """
    Saves the dashboard layout and returns a unique shareable ID.
    """
    content = request.json
    layout = content.get('layout')
    title = content.get('title')
    if not title:
        title = 'Fluxus Bi Dashboard'
    
    if not layout:
        return jsonify({"error": "Missing layout data"}), 400
        
    share_id = str(uuid.uuid4())[:8] # Short 8-char ID
    published_dashboards_db[share_id] = {
        "layout": layout,
        "title": title
    }
    
    return jsonify({"share_id": share_id}), 200

@app.route('/dashboard/<share_id>', methods=['GET'])
def get_shared_dashboard(share_id):
    """
    Retrieves a shared dashboard layout.
    """
    if share_id not in published_dashboards_db:
        return jsonify({"error": "Dashboard not found"}), 404
        
    return jsonify(published_dashboards_db[share_id]), 200

if __name__ == '__main__':
    # Ensure GROQ_API_KEY is present
    if not os.getenv("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY environment variable is not set!")
        
    app.run(debug=True, port=5000)
