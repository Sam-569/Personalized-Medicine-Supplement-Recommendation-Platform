import axios from 'axios'
export const http = axios.create({ baseURL: '/api' })
export const getToken = () => localStorage.getItem('t')
export const setToken = (t: string | null) => (t ? localStorage.setItem('t', t) : localStorage.removeItem('t'))
http.interceptors.request.use(c => { const t = getToken(); if (t) c.headers.Authorization = 'Bearer ' + t; return c })
http.interceptors.response.use(r => r, e => { if (e.response?.status === 401 && getToken()) { setToken(null); location.href = '/login' } return Promise.reject(e) })
export const errMsg = (e: any) => { const d = e.response?.data?.detail; return typeof d === 'string' ? d : Array.isArray(d) ? d.map((x: any) => x.loc.slice(-1) + ': ' + x.msg).join('; ') : 'Request failed' }
