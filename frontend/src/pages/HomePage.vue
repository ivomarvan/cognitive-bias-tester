<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <main class="mx-auto flex min-h-screen max-w-3xl flex-col items-center justify-center px-4 py-16">
    <h1
      class="mb-4 text-center text-4xl font-bold tracking-tight text-indigo-700 sm:text-5xl"
      data-testid="home-heading"
    >
      {{ t('home.heading') }}
    </h1>
    <p class="text-center text-lg text-slate-600">
      {{ t('app.title') }}
    </p>
  </main>
</template>
