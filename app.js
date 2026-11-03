
const state = {
    token: sessionStorage.getItem("access_token"),
    resumeId: Number(sessionStorage.getItem("resume_id")) || null
};

const $ = (id) => document.getElementById(id);

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

function showResult(id, html) {
    $(id).innerHTML = html;
}

function showError(id, message) {
    showResult(id, `<strong>⚠️ ${escapeHTML(message)}</strong>`);
}

function showList(items) {
    if (!items || !items.length) {
        return "<p>No information available.</p>";
    }

    return `<ul>${items.map(item =>
        `<li>${escapeHTML(item)}</li>`
    ).join("")}</ul>`;
}

function requireResume() {
    if (!state.resumeId) {
        alert("Please upload your resume first.");
        return false;
    }
    return true;
}

async function apiRequest(url, options = {}) {
    if (!state.token) {
        throw new Error("Please login first.");
    }

    const headers = {
        Authorization: `Bearer ${state.token}`,
        ...options.headers
    };

    const response = await fetch(url, {
        ...options,
        headers
    });

    if (response.status === 401) {
        sessionStorage.removeItem("access_token");
        state.token = null;
        $("dashboard").classList.add("hidden");
        $("authPanel").classList.remove("hidden");
        throw new Error("Session expired. Please login again.");
    }

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(
            error.detail || "Something went wrong."
        );
    }

    return response;
}

async function postJSON(url, data) {
    return apiRequest(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
}

function showDashboard() {
    $("authPanel").classList.add("hidden");
    $("dashboard").classList.remove("hidden");
    $("logoutBtn").hidden = false;

    $("resumeIdDisplay").textContent =
        state.resumeId || "Not uploaded";

    $("resumeStatus").textContent =
        state.resumeId ? "Uploaded" : "Pending";
}

function logout() {
    sessionStorage.removeItem("access_token");
    sessionStorage.removeItem("resume_id");

    state.token = null;
    state.resumeId = null;

    $("dashboard").classList.add("hidden");
    $("authPanel").classList.remove("hidden");
    $("logoutBtn").hidden = true;

    $("resumeIdDisplay").textContent = "Not uploaded";
    $("resumeStatus").textContent = "Pending";
}


// LOGIN / REGISTER TABS

document.querySelectorAll(".auth-tab").forEach(tab => {
    tab.addEventListener("click", () => {
        const mode = tab.dataset.auth;

        document.querySelectorAll(".auth-tab").forEach(item => {
            item.classList.remove("active");
        });

        tab.classList.add("active");

        $("loginForm").classList.toggle(
            "hidden", mode !== "login"
        );

        $("registerForm").classList.toggle(
            "hidden", mode !== "register"
        );

        $("authMessage").textContent = "";
    });
});


// REGISTER

$("registerForm").addEventListener("submit", async event => {
    event.preventDefault();

    const data = {
        full_name: $("registerName").value.trim(),
        email: $("registerEmail").value.trim(),
        password: $("registerPassword").value
    };

    try {
        const response = await fetch("/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Registration failed.");
        }

        $("authMessage").textContent =
            "✅ Registration successful! Please login.";

        $("loginEmail").value = data.email;

        document.querySelector('[data-auth="login"]').click();

        $("loginPassword").focus();

    } catch (error) {
        $("authMessage").textContent = "⚠️ " + error.message;
    }
});


// LOGIN

$("loginForm").addEventListener("submit", async event => {
    event.preventDefault();

    const data = {
        email: $("loginEmail").value.trim(),
        password: $("loginPassword").value
    };

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Login failed.");
        }

        state.token = result.access_token;

        sessionStorage.setItem(
            "access_token",
            state.token
        );

        $("authMessage").textContent = "Login successful!";

        showDashboard();

    } catch (error) {
        $("authMessage").textContent = "⚠️ " + error.message;
    }
});


// LOGOUT

$("logoutBtn").addEventListener("click", logout);


// RESUME UPLOAD

$("uploadBtn").addEventListener("click", async () => {

    const file = $("resumeFile").files[0];

    if (!file) {
        alert("Please select a PDF or DOCX resume.");
        return;
    }

    try {
        const formData = new FormData();

        formData.append("file", file);

        const response = await apiRequest("/resume/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        state.resumeId = result.resume_id;

        sessionStorage.setItem(
            "resume_id",
            state.resumeId
        );

        $("resumeIdDisplay").textContent = state.resumeId;
        $("resumeStatus").textContent = "Uploaded";

        showResult("resumeResult", `
            <h3>✅ Resume Uploaded Successfully!</h3>
            <p>Resume ID: ${escapeHTML(result.resume_id)}</p>
            <p>Filename: ${escapeHTML(result.filename)}</p>
            <p>Extracted Characters: ${escapeHTML(result.extracted_text_length)}</p>
            <h3>Resume Preview</h3>
            <p>${escapeHTML(result.text_preview)}</p>
        `);

    } catch (error) {
        showError("resumeResult", error.message);
    }
});


// RESUME PARSING

$("parseBtn").addEventListener("click", async () => {

    if (!requireResume()) return;

    try {
        const response = await apiRequest(
            `/resume/${state.resumeId}/parse`
        );

        const result = await response.json();
        const data = result.parsed_data;

        showResult("resumeResult", `
            <h3>✅ Resume Parsed Successfully</h3>
            <p><strong>Name:</strong> ${escapeHTML(data.candidate_details.name)}</p>
            <p><strong>Email:</strong> ${escapeHTML(data.candidate_details.email)}</p>
            <p><strong>Phone:</strong> ${escapeHTML(data.candidate_details.phone)}</p>
            <h3>Education</h3>
            ${showList(data.education)}
            <h3>Technical Skills</h3>
            ${showList(data.technical_skills)}
            <h3>Projects</h3>
            ${showList(data.projects)}
            <h3>Experience</h3>
            ${showList(data.experience)}
            <h3>Certifications</h3>
            ${showList(data.certifications)}
            <h3>Career Objective</h3>
            <p>${escapeHTML(data.career_objective)}</p>
        `);

    } catch (error) {
        showError("resumeResult", error.message);
    }
});


// JOB MATCHING

$("matchBtn").addEventListener("click", async () => {

    if (!requireResume()) return;

    const jobTitle = $("jobTitle").value.trim();
    const jobDescription = $("jobDescription").value.trim();

    if (!jobTitle || jobDescription.length < 30) {
        alert("Enter job title and a job description of at least 30 characters.");
        return;
    }

    try {
        const response = await postJSON("/analysis/match", {
            resume_id: state.resumeId,
            job_title: jobTitle,
            job_description: jobDescription
        });

        const result = await response.json();
        const match = result.matching_results;

        showResult("matchResult", `
            <h3>🎯 Job Matching Results</h3>
            <h2>${escapeHTML(match.overall_match_score)}% Overall Match</h2>
            <p>Skill Match: ${escapeHTML(match.skill_match_score)}%</p>
            <p>Text Similarity: ${escapeHTML(match.text_similarity_score)}%</p>
            <h3>Matched Skills</h3>
            ${showList(match.matched_skills)}
            <h3>Missing Skills</h3>
            ${showList(match.missing_skills)}
        `);

    } catch (error) {
        showError("matchResult", error.message);
    }
});


// ATS CHECKER

$("atsBtn").addEventListener("click", async () => {

    if (!requireResume()) return;

    try {
        const response = await postJSON("/analysis/ats-check", {
            resume_id: state.resumeId,
            job_title: $("jobTitle").value.trim(),
            job_description: $("jobDescription").value.trim()
        });

        const result = await response.json();
        const ats = result.ats_analysis;
        const gap = result.skill_gap_analysis;

        showResult("atsResult", `
            <h3>📊 ATS Compatibility Results</h3>
            <h2>${escapeHTML(ats.ats_compatibility_score)}%</h2>
            <p>Keyword Match: ${escapeHTML(ats.keyword_match_percentage)}%</p>
            <h3>Missing Keywords</h3>
            ${showList(ats.missing_keywords)}
            <h3>Matched Skills</h3>
            ${showList(gap.matched_skills)}
            <h3>Improvement Suggestions</h3>
            ${showList(ats.suggestions)}
        `);

    } catch (error) {
        showError("atsResult", error.message);
    }
});


// CAREER RECOMMENDATIONS

$("careerBtn").addEventListener("click", async () => {

    if (!requireResume()) return;

    try {
        const response = await postJSON(
            "/analysis/career-recommendations",
            { resume_id: state.resumeId }
        );

        const result = await response.json();

        showResult("careerResult", `
            <h3>💼 Recommended Career Roles</h3>
            ${result.recommendations.map(role => `
                <div class="stat-card" style="margin:10px 0;background:#eee9ff;color:#302a57">
                    <strong>${escapeHTML(role.job_role)}</strong>
                    <p>Match: ${escapeHTML(role.match_score)}%</p>
                    <p>Level: ${escapeHTML(role.level)}</p>
                    <p>Matched Skills: ${escapeHTML(role.matched_skills.join(", "))}</p>
                    <p>Skills to Learn: ${escapeHTML(role.skills_to_learn.join(", "))}</p>
                </div>
            `).join("")}
        `);

    } catch (error) {
        showError("careerResult", error.message);
    }
});


// WHAT-IF SIMULATOR

$("simulateBtn").addEventListener("click", async () => {

    if (!requireResume()) return;

    const additionalSkills = $("additionalSkills").value
        .split(",")
        .map(skill => skill.trim())
        .filter(Boolean);

    try {
        const response = await postJSON("/simulator/what-if", {
            resume_id: state.resumeId,
            job_role: $("simulatorRole").value,
            additional_skills: additionalSkills
        });

        const result = await response.json();
        const simulation = result.simulation_results;

        showResult("simulatorResult", `
            <h3>🔮 Simulation Results</h3>
            <p>Current Match: <strong>${escapeHTML(simulation.current_match_score)}%</strong></p>
            <p>Projected Match: <strong>${escapeHTML(simulation.projected_match_score)}%</strong></p>
            <p>Improvement: <strong>${escapeHTML(simulation.score_improvement)} percentage points</strong></p>
            <h3>Newly Matched Skills</h3>
            ${showList(simulation.newly_matched_skills)}
            <h3>Skills Still to Learn</h3>
            ${showList(simulation.remaining_skills_to_learn)}
        `);

    } catch (error) {
        showError("simulatorResult", error.message);
    }
});


// INTERVIEW PREPARATION

$("interviewBtn").addEventListener("click", async () => {

    if (!requireResume()) return;

    try {
        const response = await postJSON("/interview/prepare", {
            resume_id: state.resumeId,
            job_role: $("interviewRole").value
        });

        const result = await response.json();
        const data = result.interview_preparation;

        const allQuestions = [
            ...data.technical_questions,
            ...data.project_questions,
            ...data.behavioral_questions
        ];

        showResult("interviewResult", `
            <h3>🎤 Interview Preparation</h3>
            <p>Total Questions: ${escapeHTML(data.total_questions)}</p>
            ${allQuestions.map((item, index) => `
                <div style="padding:12px;border-bottom:1px solid #ddd">
                    <strong>Q${index + 1}. ${escapeHTML(item.question)}</strong>
                    <p>Category: ${escapeHTML(item.category)}</p>
                    <p>Difficulty: ${escapeHTML(item.difficulty)}</p>
                    <p><strong>Sample Answer:</strong> ${escapeHTML(item.sample_answer)}</p>
                </div>
            `).join("")}
        `);

    } catch (error) {
        showError("interviewResult", error.message);
    }
});


// LEARNING ROADMAP

$("roadmapBtn").addEventListener("click", async () => {

    if (!requireResume()) return;

    try {
        const response = await postJSON("/roadmap/generate", {
            resume_id: state.resumeId,
            job_role: $("roadmapRole").value
        });

        const result = await response.json();
        const roadmap = result.learning_roadmap;

        showResult("roadmapResult", `
            <h3>📚 Personalized Learning Roadmap</h3>
            <p>Career Role: ${escapeHTML(roadmap.job_role)}</p>
            <p>Estimated Duration: ${escapeHTML(roadmap.estimated_duration_weeks)} weeks</p>
            ${roadmap.weekly_learning_roadmap.map(week => `
                <div style="padding:15px;margin:10px 0;background:#eee9ff;border-radius:12px">
                    <h3>Week ${escapeHTML(week.week)} – ${escapeHTML(week.skill_to_learn)}</h3>
                    <p>Topics: ${escapeHTML(week.learning_topics.join(", "))}</p>
                    <p>Practice: ${escapeHTML(week.practice_task)}</p>
                    <p>Resource: ${escapeHTML(week.recommended_resource)}</p>
                </div>
            `).join("")}
            <p><strong>Final Project:</strong> ${escapeHTML(roadmap.final_capstone_project)}</p>
        `);

    } catch (error) {
        showError("roadmapResult", error.message);
    }
});


// PDF REPORT GENERATION

$("reportBtn").addEventListener("click", async () => {

    if (!requireResume()) return;

    try {
        const response = await postJSON("/reports/generate", {
            resume_id: state.resumeId,
            job_title: $("jobTitle").value.trim(),
            target_role: $("roadmapRole").value,
            job_description: $("jobDescription").value.trim()
        });

        const blob = await response.blob();

        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;
        link.download = "AI_Career_Intelligence_Report.pdf";

        document.body.appendChild(link);

        link.click();
        link.remove();

        URL.revokeObjectURL(url);

        showResult("reportResult",
            "<h3>✅ PDF Report Generated Successfully!</h3>"
        );

    } catch (error) {
        showError("reportResult", error.message);
    }
});


// RESTORE SESSION

if (state.token) {
    showDashboard();
}

if (state.resumeId) {
    $("resumeIdDisplay").textContent = state.resumeId;
    $("resumeStatus").textContent = "Uploaded";
}
