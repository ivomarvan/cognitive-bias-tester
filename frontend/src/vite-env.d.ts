/// <reference types="vite/client" />

declare module '*.json' {
  /** Locale bundle shape for this app (en/cs). */
  const value: {
    app: { title: string }
    home: { heading: string }
  }
  export default value
}
