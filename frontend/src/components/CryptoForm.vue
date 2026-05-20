<template>
  <div class="max-w-md mx-auto my-12 p-8 bg-slate-900 text-white rounded-2xl shadow-2xl border border-slate-800">

    <h1 class="text-2xl font-bold text-center text-emerald-400 mb-6">
      AES Cryptographer
    </h1>

    <div class="flex gap-2 mb-6">
      <button
        type="button"
        @click="setMode('encrypt')"
        :class="mode === 'encrypt' ? 'bg-emerald-500 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'"
        class="flex-1 py-2.5 font-semibold rounded-lg text-center transition"
      >
        Encrypt
      </button>
      <button
        type="button"
        @click="setMode('decrypt')"
        :class="mode === 'decrypt' ? 'bg-emerald-500 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'"
        class="flex-1 py-2.5 font-semibold rounded-lg text-center transition"
      >
        Decrypt
      </button>
    </div>

    <form @submit.prevent="submitForm" class="space-y-5">

      <div class="flex flex-col gap-2">
        <label class="text-sm font-medium text-slate-300">Choose or drop file:</label>

        <div
          @click="$refs.fileInput.click()"
          @dragenter.prevent="isDragging = true"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleFileDrop"
          :class="isDragging ? 'border-emerald-400 bg-emerald-500/10' : 'border-slate-700 bg-slate-800/50 hover:border-slate-600'"
          class="flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-xl transition cursor-pointer group"
        >
          <input
            type="file"
            ref="fileInput"
            @change="handleFileChange"
            class="hidden"
          />

          <span class="text-3xl mb-2 transition group-hover:scale-110 duration-200 pointer-events-none">
            {{ file ? '📄' : '📁' }}
          </span>

          <p class="text-sm font-medium text-slate-300 text-center pointer-events-none">
            {{ file ? file.name : 'Drag and drop your file here' }}
          </p>
          <p v-if="!file" class="text-xs text-slate-500 mt-1 pointer-events-none">or click to browse</p>
        </div>
      </div>

      <div class="flex flex-col gap-2">
        <label class="text-sm font-medium text-slate-300">Enter password (min. 8 characters):</label>
        <input
          type="password"
          v-model="password"
          placeholder="Enter a secure password"
          required
          class="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
        />
      </div>

      <button
        type="submit"
        :disabled="loading || !file"
        class="w-full py-3 bg-emerald-500 hover:bg-emerald-600 font-bold rounded-lg shadow-lg shadow-emerald-500/20 transition disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed"
      >
        {{ buttonText }}
      </button>

    </form>

    <div v-if="error" class="mt-5 p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-sm font-medium">
      ⚠️ {{ error }}
    </div>

  </div>
</template>

<script setup>
import { toRefs } from 'vue'
import { useCrypto } from '../composables/useCrypto'

const cryptoState = useCrypto()
const { mode, password, loading, error, isDragging, file, buttonText } = toRefs(cryptoState)
const { setMode, handleFileChange, handleFileDrop, submitForm } = cryptoState
</script>