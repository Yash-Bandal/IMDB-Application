import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import '@fontsource/roboto/400.css'
import '@fontsource/roboto/500.css'
import '@fontsource/roboto/700.css'

import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
  },
  icons: {
    defaultSet: 'mdi',
  },
    defaults: {
    global: {
      style: {
        fontFamily: 'Roboto, sans-serif',
      },
    },
  },
})
