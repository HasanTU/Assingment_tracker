import { CONFIG } from './config.js';
import { uploadFile } from './main.js';

async function uploadSubmissionFile(){
    const assignmentId = "1"
    const courseId = "1"

    const dict = {
        "assignment_id":assignmentId,
        "course_id":courseId
    }

    uploadFile('student-file', 'student', "/submission", dict)
}

window.uploadSubmissionFile = uploadSubmissionFile;