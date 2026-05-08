import { mount } from '@vue/test-utils'
import { createI18n } from 'vue-i18n'
import { describe, expect, it } from 'vitest'

import cs from '@/locales/cs.json'
import en from '@/locales/en.json'
import HomePage from './HomePage.vue'

function createTestI18n(locale: string) {
  return createI18n({
    legacy: false,
    locale,
    fallbackLocale: 'en',
    messages: {
      en,
      cs,
    },
  })
}

describe('HomePage', () => {
  it('shows the English welcome heading', () => {
    const i18n = createTestI18n('en')
    const wrapper = mount(HomePage, {
      global: { plugins: [i18n] },
    })

    expect(wrapper.get('[data-testid="home-heading"]').text()).toBe(en.home.heading)
    expect(wrapper.text()).toContain(en.app.title)
  })

  it('shows the Czech welcome heading when locale is cs', () => {
    const i18n = createTestI18n('cs')
    const wrapper = mount(HomePage, {
      global: { plugins: [i18n] },
    })

    expect(wrapper.get('[data-testid="home-heading"]').text()).toBe(cs.home.heading)
    expect(wrapper.text()).toContain(cs.app.title)
  })
})
