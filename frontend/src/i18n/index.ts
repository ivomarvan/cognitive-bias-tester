import { createI18n } from 'vue-i18n'

import cs from '@/locales/cs.json'
import en from '@/locales/en.json'

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    cs,
  },
})
