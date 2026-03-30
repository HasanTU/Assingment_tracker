import {defineConfig} from 'vite';
import path from 'path';

export default defineConfig({
// 1. บอก Vite ว่า "หน้าตึก" ของเราอยู่ในโฟลเดอร์ src นะ
  root: 'src',

  resolve: {
    alias: {
      // 2. ตั้งค่า @ ให้ชี้ไปที่โฟลเดอร์ src 
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    hmr: process.env.DISABLE_HMR !== 'true',
  },
});
