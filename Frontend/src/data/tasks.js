// ===========================
// data/tasks.js
// ข้อมูลส่วนนี้ — backend เปลี่ยนมาดึงจาก API ได้เลย
// ===========================

var tasks = [
  { id: 1, name: 'Assignment 5',    course: 'CS222', due: '1 Apr 2026',  status: 'late',    desc: 'จงทำการออกแบบเกมที่คุณได้เล่นไปล่าสุดแล้วนำมาส่งผมด้วยนะครับ' },
  { id: 2, name: 'Assignment 3',    course: 'CS232', due: '7 Apr 2026',  status: 'pending', desc: 'วิเคราะห์ความซับซ้อนของ Sorting Algorithms อย่างน้อย 3 แบบ พร้อมตัวอย่าง code' },
  { id: 3, name: 'Lab Report 2',    course: 'CS251', due: '10 Apr 2026', status: 'pending', desc: 'จัดทำรายงานผลการทดลองเรื่อง Process Scheduling ในระบบปฏิบัติการ' },
  { id: 4, name: 'Quiz 4',          course: 'CS271', due: '12 Apr 2026', status: 'pending', desc: 'ทำแบบทดสอบบทที่ 4 เรื่อง Network Layer ผ่านระบบ MS Teams' },
  { id: 5, name: 'Project Phase 1', course: 'CS242', due: '2 Apr 2026',  status: 'done',    desc: 'ส่ง proposal โปรเจกต์ Database พร้อม ER Diagram' },
  { id: 6, name: 'Homework 6',      course: 'CS222', due: '2 Apr 2026',  status: 'done',    desc: 'แก้โจทย์ Graph Theory ข้อ 1-10 จากใบงานที่แจก' },
  { id: 7, name: 'Assignment 2',    course: 'EL395', due: '28 Mar 2026', status: 'done',    desc: 'เขียนรายงานสรุปบทความวิชาการ 1 หน้า A4' },
  { id: 8, name: 'Lab 3',           course: 'CS217', due: '25 Mar 2026', status: 'done',    desc: 'ทดลองและรายงานผลการทดลองวงจรดิจิทัลพื้นฐาน' },
];

// summary stats (นับรวม — backend คำนวณให้ได้เลย)
var statsByAll = { done: 23, pending: 15, late: 3 };

// stats แยกตามวิชา
var statsByCourse = {
  'CS232': { done: 6, pending: 1, late: 0 },
  'CS251': { done: 4, pending: 2, late: 0 },
  'CS222': { done: 8, pending: 0, late: 1 },
  'CS271': { done: 2, pending: 1, late: 0 },
  'CS242': { done: 1, pending: 0, late: 0 },
  'CS217': { done: 1, pending: 0, late: 0 },
  'EL395': { done: 1, pending: 0, late: 0 },
};



// async function loadTasks() {
//   try {
//     const res = await fetch(`${CONFIG.BACKEND_API_URL}`);
//     const data = await res.json();

//     // สมมติ backend ส่งมาแบบนี้
//     // { tasks: [...], statsByAll: {...}, statsByCourse: {...} }

//     const tasks = data.tasks;
//     const statsByAll = data.statsByAll;
//     const statsByCourse = data.statsByCourse;

//     console.log(tasks);
//     console.log(statsByAll);
//     console.log(statsByCourse);

//     // 👉 เอาไป render UI ต่อ
//     renderTasks(tasks);
//     renderStats(statsByAll, statsByCourse);

//   } catch (err) {
//     console.error("โหลดข้อมูลไม่สำเร็จ", err);
//   }
// }