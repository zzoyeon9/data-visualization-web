import Vue from 'vue'
import Router from 'vue-router'
import { normalizeURL, decode } from 'ufo'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _2d3ae171 = () => interopDefault(import('..\\pages\\vision\\CpkPage.vue' /* webpackChunkName: "pages/vision/CpkPage" */))
const _7b6fc8dc = () => interopDefault(import('..\\pages\\vision\\ScatterPlotPage.vue' /* webpackChunkName: "pages/vision/ScatterPlotPage" */))
const _4d3ad50e = () => interopDefault(import('..\\pages\\vision\\SpcPage.vue' /* webpackChunkName: "pages/vision/SpcPage" */))
const _70e7c120 = () => interopDefault(import('..\\pages\\vision\\TrendPage.vue' /* webpackChunkName: "pages/vision/TrendPage" */))
const _6481b404 = () => interopDefault(import('..\\pages\\index.vue' /* webpackChunkName: "pages/index" */))

const emptyFn = () => {}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: '/',
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/vision/CpkPage",
    component: _2d3ae171,
    name: "vision-CpkPage"
  }, {
    path: "/vision/ScatterPlotPage",
    component: _7b6fc8dc,
    name: "vision-ScatterPlotPage"
  }, {
    path: "/vision/SpcPage",
    component: _4d3ad50e,
    name: "vision-SpcPage"
  }, {
    path: "/vision/TrendPage",
    component: _70e7c120,
    name: "vision-TrendPage"
  }, {
    path: "/",
    component: _6481b404,
    name: "index"
  }],

  fallback: false
}

export function createRouter (ssrContext, config) {
  const base = (config._app && config._app.basePath) || routerOptions.base
  const router = new Router({ ...routerOptions, base  })

  // TODO: remove in Nuxt 3
  const originalPush = router.push
  router.push = function push (location, onComplete = emptyFn, onAbort) {
    return originalPush.call(this, location, onComplete, onAbort)
  }

  const resolve = router.resolve.bind(router)
  router.resolve = (to, current, append) => {
    if (typeof to === 'string') {
      to = normalizeURL(to)
    }
    return resolve(to, current, append)
  }

  return router
}
