export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'myProject',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/proxy',
  ],

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    extend(config, { isClient }) {
      // ...
      config.module.rules.push({
        test: /\.js$/,
        loader: 'babel-loader',
      exclude: [ /node_modules\\babel*/, /node_modules\\@babel*/, /node_modules\\webpack*/, /node_modules\\vue-loader/, /node_modules\\css-loader/]
      });
    },
  },


  axios: {
    proxy: true,
  },

  // proxy: {
  //   '/api/': {
  //     target: process.env.API_DEV,
  //     pathRewrite: {'^/api': ''},
  //     changeOrigin: true
  //   }
  // }
  
  proxy: {
    '/api/': {
      target: 'http://10.0.1.47:30000',
      pathRewrite: {
        '^/api/': ''
      }
    } 
  },
}
