<template>
  <div class="min-h-screen flex items-stretch text-gray-900 overflow-hidden bg-gray-50">
    
    <!-- Left Side: Visual/Branding -->
    <div class="hidden lg:flex w-1/2 relative flex-col justify-center items-center overflow-hidden">
      <!-- Background Gradients -->
      <div class="absolute inset-0 bg-gradient-to-br from-indigo-900 to-slate-900 z-0"></div>
      <div class="absolute top-0 right-0 w-[500px] h-[500px] bg-blue-500 rounded-full mix-blend-multiply filter blur-[100px] opacity-40 animate-blob"></div>
      <div class="absolute bottom-0 left-0 w-[500px] h-[500px] bg-purple-500 rounded-full mix-blend-multiply filter blur-[100px] opacity-40 animate-blob animation-delay-2000"></div>
      
      <!-- Content -->
      <div class="z-10 text-center px-12 text-white max-w-lg">
        <div class="flex items-center justify-center space-x-6 mb-8">
          <div class="w-20 h-20 bg-white/10 backdrop-blur-lg rounded-2xl flex items-center justify-center border border-white/20 shadow-2xl shrink-0">
            <svg class="w-10 h-10 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          </div>
          <h2 class="text-5xl font-extrabold tracking-wider whitespace-nowrap">Fluxus Bi</h2>
        </div>
        <h1 class="text-4xl font-bold mb-6 tracking-tight leading-tight">Smart Business<br>Intelligence</h1>
        <p class="text-lg text-indigo-200 mb-8 leading-relaxed">
          Upload data, instantly visualize insights, and chat with an AI analytics master—all in one place.
        </p>
        
        <div class="flex items-center justify-center space-x-3 text-sm text-indigo-300/80 font-medium tracking-wider">
          <span class="w-8 h-[1px] bg-indigo-400/50"></span>
          <span>Powered by Vue 3 & LangChain</span>
          <span class="w-8 h-[1px] bg-indigo-400/50"></span>
        </div>
      </div>
    </div>

    <!-- Right Side: Login Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center bg-white p-8 sm:p-12 lg:p-24 shadow-[-20px_0_40px_rgba(0,0,0,0.05)] z-10">
      <div class="w-full max-w-md space-y-8">
        
        <div class="text-center lg:text-left">
          <h2 class="text-3xl font-extrabold text-gray-900 tracking-tight">Welcome back</h2>
          <p class="mt-3 text-sm text-gray-500">
            Sign in to access your dashboards and AI insights.
          </p>
        </div>

        <!-- Google Login Block -->
        <div class="mt-8">
          <div class="flex justify-center lg:justify-start">
            <!-- Mock Google Login Button -->
            <button type="button" @click="handleGoogleMockClick" class="w-full lg:w-auto flex items-center justify-center px-8 py-3.5 border border-gray-300 rounded-xl shadow-sm bg-white text-sm font-semibold text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 ease-in-out hover:shadow-md">
              <svg class="h-5 w-5 mr-3" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/><path d="M1 1h22v22H1z" fill="none"/></svg>
              Continue with Google
            </button>
          </div>
        </div>

        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-3 bg-white text-gray-500">Or continue with email</span>
          </div>
        </div>

        <!-- Classic Form -->
        <form class="space-y-5" @submit.prevent="handleEmailLogin">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
            <div class="mt-1 relative rounded-md shadow-sm">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path></svg>
              </div>
              <input id="email" v-model="email" type="email" required class="block w-full pl-10 px-4 py-3 border border-gray-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm outline-none transition-shadow" placeholder="you@example.com">
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <div class="mt-1 relative rounded-md shadow-sm">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
              </div>
              <input id="password" v-model="password" type="password" required class="block w-full pl-10 px-4 py-3 border border-gray-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm outline-none transition-shadow" placeholder="••••••••">
            </div>
          </div>

          <div class="flex items-center justify-between mt-4">
            <div class="flex items-center">
              <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded cursor-pointer">
              <label for="remember-me" class="ml-2 block text-sm text-gray-700 cursor-pointer">
                Remember me
              </label>
            </div>
            <div class="text-sm">
              <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500 transition-colors">Forgot your password?</a>
            </div>
          </div>

          <div>
            <button type="submit" class="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200">
              Sign in
            </button>
          </div>
        </form>
        
        

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

const loginSuccess = () => {
  // Mock login logic: Set token and redirect
  localStorage.setItem('auth_token', 'mock_dummy_token_12345')
  router.push('/dashboard')
}

const handleEmailLogin = () => {
  if (email.value && password.value) {
    loginSuccess()
  }
}

// Called when Mock Google OAuth button is clicked
const handleGoogleMockClick = () => {
  console.log("Mock Google Login Triggered")
  loginSuccess()
}
</script>

<style scoped>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
</style>
