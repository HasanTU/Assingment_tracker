// ===========================
// data/tasks.js
// ข้อมูลส่วนนี้ — backend เปลี่ยนมาดึงจาก API ได้เลย
// ===========================

// var tasks = [
//   { id: 1, name: 'Assignment 5',    course: 'CS222', due: '1 Apr 2026',  status: 'late',    desc: 'จงทำการออกแบบเกมที่คุณได้เล่นไปล่าสุดแล้วนำมาส่งผมด้วยนะครับ' },
//   { id: 2, name: 'Assignment 3',    course: 'CS232', due: '7 Apr 2026',  status: 'pending', desc: 'วิเคราะห์ความซับซ้อนของ Sorting Algorithms อย่างน้อย 3 แบบ พร้อมตัวอย่าง code' },
//   { id: 3, name: 'Lab Report 2',    course: 'CS251', due: '10 Apr 2026', status: 'pending', desc: 'จัดทำรายงานผลการทดลองเรื่อง Process Scheduling ในระบบปฏิบัติการ' },
//   { id: 4, name: 'Quiz 4',          course: 'CS271', due: '12 Apr 2026', status: 'pending', desc: 'ทำแบบทดสอบบทที่ 4 เรื่อง Network Layer ผ่านระบบ MS Teams' },
//   { id: 5, name: 'Project Phase 1', course: 'CS242', due: '2 Apr 2026',  status: 'done',    desc: 'ส่ง proposal โปรเจกต์ Database พร้อม ER Diagram' },
//   { id: 6, name: 'Homework 6',      course: 'CS222', due: '2 Apr 2026',  status: 'done',    desc: 'แก้โจทย์ Graph Theory ข้อ 1-10 จากใบงานที่แจก' },
//   { id: 7, name: 'Assignment 2',    course: 'EL395', due: '28 Mar 2026', status: 'done',    desc: 'เขียนรายงานสรุปบทความวิชาการ 1 หน้า A4' },
//   { id: 8, name: 'Lab 3',           course: 'CS217', due: '25 Mar 2026', status: 'done',    desc: 'ทดลองและรายงานผลการทดลองวงจรดิจิทัลพื้นฐาน' },
// ];

var tasks = [
];

var courses = [];

function formatDate(datetimeStr) {
  const date = new Date(datetimeStr);

  const months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];

  const day = date.getDate();
  const month = months[date.getMonth()];
  const year = date.getFullYear();

  return `${day} ${month} ${year}`;
}

function mapStatus(status) {
  switch (status) {
    case "PENDING":
      return "pending";
    case "SUBMITTED":
      return "done";
    case "GRADED":
      return "done";
    case "OVERDUE":
      return "late";
    default:
      return "pending";
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    console.log("Starting fetch...");
    const response = await fetch(`${APP.CONFIG.BACKEND_API_URL}/api/tasks`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        
        credentials: "include"
    });

    console.log("Response received:", response.status);
    const jsonData = await response.json()
    const data = jsonData.data;
    console.log("Data parsed:", data);


    if (response.ok) {
      tasks = data.map(item => {
      return {
        id: item.assignment_id,
        name: item.title,
        course: item.course_name,
        desc: item.description,
        status: mapStatus(item.status.toUpperCase()), // pending / submitted / graded / overdue
        due: formatDate(item.deadline),
        source_url: item.source_url
      };
    });

      courses = [...new Set(tasks.map(t => t.course))];

    } else {
      console.log("")
    }
  } catch (err) {
      console.error("Fetch Error Detail:", err);
  }
  finally{
    const debug_tasks = tasks.map(t => ({
      title: t.name,
      status: t.status
    }));

    console.log("Debug tasks: ", debug_tasks)
    renderCourses()
    renderTasks()
    
    //window.dispatchEvent(new Event("tasksLoaded"));
  }
})


// var statsByAll = tasks.reduce(function(acc, t) {
//   acc[t.status] = (acc[t.status] || 0) + 1;
//   return acc;
// }, { done: 0, pending: 0, late: 0 });

// var statsByCourse = tasks.reduce(function(acc, t) {
//   if (!acc[t.course]) acc[t.course] = { done: 0, pending: 0, late: 0 };
//   acc[t.course][t.status] = (acc[t.course][t.status] || 0) + 1;
//   return acc;
// }, {});