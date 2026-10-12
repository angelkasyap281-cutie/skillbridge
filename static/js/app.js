/**
 * app.js - SkillBridge AI Client-Side Application Logic
 * Handles interactive skill tags, preset role population, asynchronous API calls,
 * animated circular progress meter, results rendering, and roadmap export.
 */

document.addEventListener("DOMContentLoaded", () => {
    // State management
    let userSkills = ["Python", "JavaScript", "HTML & CSS", "Git & GitHub"];
    const sampleRoles = window.INITIAL_SAMPLE_ROLES || [];

    // DOM Elements
    const skillInput = document.getElementById("skillInput");
    const tagsWrapper = document.getElementById("tagsWrapper");
    const skillCounter = document.getElementById("skillCounter");
    const clearSkillsBtn = document.getElementById("clearSkillsBtn");
    const popularPills = document.querySelectorAll(".pill-btn");

    const jobDescriptionInput = document.getElementById("jobDescriptionInput");
    const charCounter = document.getElementById("charCounter");
    const clearJdBtn = document.getElementById("clearJdBtn");
    const sampleFillBtn = document.getElementById("sampleFillBtn");

    const presetButtons = document.querySelectorAll(".preset-btn");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const resetBtn = document.getElementById("resetBtn");
    const loadingState = document.getElementById("loadingState");
    const alertBox = document.getElementById("alertBox");
    const alertMessage = document.getElementById("alertMessage");

    const resultsSection = document.getElementById("resultsSection");
    const scoreProgressCircle = document.getElementById("scoreProgressCircle");
    const scoreValue = document.getElementById("scoreValue");
    const readinessBadge = document.getElementById("readinessBadge");
    const readinessTitle = document.getElementById("readinessTitle");
    const readinessDesc = document.getElementById("readinessDesc");

    const kpiMatchScore = document.getElementById("kpiMatchScore");
    const kpiMatchedCount = document.getElementById("kpiMatchedCount");
    const kpiMissingCount = document.getElementById("kpiMissingCount");
    const kpiEstTime = document.getElementById("kpiEstTime");

    const matchedCountTag = document.getElementById("matchedCountTag");
    const missingCountTag = document.getElementById("missingCountTag");
    const bonusCountTag = document.getElementById("bonusCountTag");

    const matchedSkillsList = document.getElementById("matchedSkillsList");
    const missingSkillsList = document.getElementById("missingSkillsList");
    const bonusSkillsList = document.getElementById("bonusSkillsList");

    const recommendationCardsGrid = document.getElementById("recommendationCardsGrid");
    const roadmapTimeline = document.getElementById("roadmapTimeline");
    const roadmapDurationText = document.getElementById("roadmapDurationText");

    const printRoadmapBtn = document.getElementById("printRoadmapBtn");
    const copySummaryBtn = document.getElementById("copySummaryBtn");

    let lastAnalysisData = null;

    // ==========================================
    // 1. Skill Tags Management
    // ==========================================

    function renderTags() {
        tagsWrapper.innerHTML = "";
        userSkills.forEach((skill, index) => {
            const tag = document.createElement("span");
            tag.className = "skill-tag";
            tag.innerHTML = `
                <span>${escapeHtml(skill)}</span>
                <span class="tag-remove" data-index="${index}" title="Remove skill">&times;</span>
            `;
            tagsWrapper.appendChild(tag);
        });

        // Update skill counter
        const count = userSkills.length;
        skillCounter.textContent = `${count} ${count === 1 ? "skill" : "skills"} added`;

        // Update popular pills highlight state
        popularPills.forEach(pill => {
            const pillSkill = pill.getAttribute("data-skill");
            if (userSkills.some(s => s.toLowerCase() === pillSkill.toLowerCase())) {
                pill.classList.add("added");
                pill.textContent = `✓ ${pillSkill}`;
            } else {
                pill.classList.remove("added");
                pill.textContent = `+ ${pillSkill}`;
            }
        });
    }

    function addSkill(skillName) {
        const cleanName = skillName.trim();
        if (!cleanName) return;

        // Check if skill already exists (case-insensitive)
        const exists = userSkills.some(s => s.toLowerCase() === cleanName.toLowerCase());
        if (!exists) {
            userSkills.push(cleanName);
            renderTags();
        }
    }

    function removeSkill(index) {
        userSkills.splice(index, 1);
        renderTags();
    }

    // Input keyboard event handler (Enter or Comma)
    skillInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === ",") {
            e.preventDefault();
            const val = skillInput.value;
            if (val.includes(",")) {
                val.split(",").forEach(s => addSkill(s));
            } else {
                addSkill(val);
            }
            skillInput.value = "";
        } else if (e.key === "Backspace" && skillInput.value === "" && userSkills.length > 0) {
            // Remove last skill on backspace in empty input
            removeSkill(userSkills.length - 1);
        }
    });

    // Handle blur event to add pending typed skill
    skillInput.addEventListener("blur", () => {
        if (skillInput.value.trim()) {
            addSkill(skillInput.value);
            skillInput.value = "";
        }
    });

    // Click on remove button inside tags wrapper
    tagsWrapper.addEventListener("click", (e) => {
        if (e.target.classList.contains("tag-remove")) {
            const idx = parseInt(e.target.getAttribute("data-index"), 10);
            removeSkill(idx);
        }
    });

    // Focus input when clicking tag container
    document.getElementById("skillTagContainer").addEventListener("click", (e) => {
        if (e.target.tagName !== "SPAN") {
            skillInput.focus();
        }
    });

    // Clear all skills
    clearSkillsBtn.addEventListener("click", () => {
        userSkills = [];
        renderTags();
        skillInput.focus();
    });

    // Quick-add pill clicks
    popularPills.forEach(pill => {
        pill.addEventListener("click", () => {
            const skillName = pill.getAttribute("data-skill");
            const existingIdx = userSkills.findIndex(s => s.toLowerCase() === skillName.toLowerCase());
            if (existingIdx >= 0) {
                // Toggle off
                removeSkill(existingIdx);
            } else {
                // Add
                addSkill(skillName);
            }
        });
    });

    // ==========================================
    // 2. Job Description Input
    // ==========================================

    function updateCharCounter() {
        const count = jobDescriptionInput.value.length;
        charCounter.textContent = `${count} characters`;
    }

    jobDescriptionInput.addEventListener("input", updateCharCounter);

    clearJdBtn.addEventListener("click", () => {
        jobDescriptionInput.value = "";
        updateCharCounter();
        jobDescriptionInput.focus();
    });

    sampleFillBtn.addEventListener("click", () => {
        if (sampleRoles.length > 0) {
            loadPresetRole(sampleRoles[0]);
        }
    });

    // ==========================================
    // 3. Preset Roles Quick Loader
    // ==========================================

    function loadPresetRole(role) {
        if (!role) return;

        // Populate Job Description
        jobDescriptionInput.value = role.description;
        updateCharCounter();

        // Populate typical skills
        if (role.typical_user_skills && Array.isArray(role.typical_user_skills)) {
            userSkills = [...role.typical_user_skills];
            renderTags();
        }

        // Highlight active preset button
        presetButtons.forEach(btn => {
            if (btn.getAttribute("data-role-id") === role.id) {
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        });

        hideAlert();
    }

    presetButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const roleId = btn.getAttribute("data-role-id");
            const role = sampleRoles.find(r => r.id === roleId);
            if (role) {
                loadPresetRole(role);
            }
        });
    });

    // ==========================================
    // 4. Analyze Skills API Interaction
    // ==========================================

    function showAlert(msg) {
        alertMessage.textContent = msg;
        alertBox.style.display = "flex";
        alertBox.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    function hideAlert() {
        alertBox.style.display = "none";
    }

    analyzeBtn.addEventListener("click", async () => {
        hideAlert();

        const jdText = jobDescriptionInput.value.trim();

        if (userSkills.length === 0 && !jdText) {
            showAlert("Please add some skills and paste a target job description to begin.");
            return;
        }

        if (!jdText) {
            showAlert("Please paste a target job description or click one of the quick sample roles above.");
            return;
        }

        // Show loading state
        loadingState.style.display = "block";
        resultsSection.style.display = "none";
        analyzeBtn.disabled = true;
        analyzeBtn.style.opacity = "0.7";

        try {
            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_skills: userSkills,
                    job_description: jdText
                })
            });

            const result = await response.json();

            if (!result.success) {
                showAlert(result.error || "Analysis failed. Please check inputs.");
                return;
            }

            // Successfully received analysis
            lastAnalysisData = result.data;
            renderAnalysisResults(result.data);

        } catch (error) {
            console.error("Network or API error:", error);
            showAlert("Unable to connect to the analysis engine. Please try again.");
        } finally {
            loadingState.style.display = "none";
            analyzeBtn.disabled = false;
            analyzeBtn.style.opacity = "1";
        }
    });

    // ==========================================
    // 5. Results Rendering & Visualizations
    // ==========================================

    function renderAnalysisResults(data) {
        resultsSection.style.display = "block";

        // Animate circular match gauge
        const circumference = 339.29; // 2 * PI * 54
        const targetPercent = data.match_percentage;
        const offset = circumference - (targetPercent / 100) * circumference;
        
        // Reset stroke offset first
        scoreProgressCircle.style.strokeDashoffset = circumference;
        setTimeout(() => {
            scoreProgressCircle.style.strokeDashoffset = offset;
        }, 80);

        // Animate counter text from 0 to targetPercent
        animateCounter(scoreValue, targetPercent, "%");

        // Banner Readiness Info
        readinessBadge.textContent = data.readiness_status;
        readinessBadge.className = `readiness-badge ${data.readiness_badge}`;
        readinessTitle.textContent = `${targetPercent}% Match with Job Requirements`;
        readinessDesc.textContent = data.readiness_message;

        // KPI Summary Cards
        kpiMatchScore.textContent = `${targetPercent}%`;
        kpiMatchedCount.textContent = data.matched_count;
        kpiMissingCount.textContent = data.missing_count;
        kpiEstTime.textContent = data.estimated_time_text.split("(")[0].trim();

        // Count tags
        matchedCountTag.textContent = `${data.matched_count} skills`;
        missingCountTag.textContent = `${data.missing_count} skills`;
        bonusCountTag.textContent = `${data.bonus_count} skills`;

        // Render Matched Skills
        matchedSkillsList.innerHTML = "";
        if (data.matched_skills.length === 0) {
            matchedSkillsList.innerHTML = `<span class="empty-chip-state">No matching skills detected yet. Follow the roadmap below!</span>`;
        } else {
            data.matched_skills.forEach(s => {
                const chip = document.createElement("span");
                chip.className = "chip-result chip-matched";
                chip.innerHTML = `<i class="fa-solid fa-check"></i> ${escapeHtml(s.name)}`;
                matchedSkillsList.appendChild(chip);
            });
        }

        // Render Missing Skills
        missingSkillsList.innerHTML = "";
        if (data.missing_skills.length === 0) {
            missingSkillsList.innerHTML = `<span class="empty-chip-state">🎉 You have all the skills required by this job description!</span>`;
        } else {
            data.missing_skills.forEach(s => {
                const chip = document.createElement("span");
                const isHigh = s.priority === "High";
                chip.className = `chip-result chip-missing ${isHigh ? 'chip-priority-high' : ''}`;
                chip.innerHTML = `
                    <i class="fa-solid fa-circle-exclamation"></i> 
                    ${escapeHtml(s.name)} 
                    <small style="opacity: 0.8; font-size: 0.7rem; margin-left: 2px;">(${s.priority})</small>
                `;
                missingSkillsList.appendChild(chip);
            });
        }

        // Render Bonus Skills
        bonusSkillsList.innerHTML = "";
        const allBonus = [
            ...data.bonus_skills.map(s => s.name),
            ...(data.custom_user_skills || [])
        ];

        if (allBonus.length === 0) {
            bonusSkillsList.innerHTML = `<span class="empty-chip-state">No additional bonus skills listed.</span>`;
        } else {
            allBonus.forEach(name => {
                const chip = document.createElement("span");
                chip.className = "chip-result chip-bonus";
                chip.innerHTML = `<i class="fa-solid fa-star"></i> ${escapeHtml(name)}`;
                bonusSkillsList.appendChild(chip);
            });
        }

        // Render Recommended Skills Cards
        renderRecommendationCards(data.recommended_skills);

        // Render Roadmap Timeline
        renderRoadmap(data.roadmap, data.estimated_time_text);

        // Smooth scroll down to results
        resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function renderRecommendationCards(skills) {
        recommendationCardsGrid.innerHTML = "";

        if (!skills || skills.length === 0) {
            recommendationCardsGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 24px;">
                    <i class="fa-solid fa-circle-check" style="color: var(--accent-emerald); font-size: 2rem; margin-bottom: 8px;"></i>
                    <p>No missing skills to recommend! You match all listed requirements.</p>
                </div>
            `;
            return;
        }

        // Take top 6 prioritized missing skills
        skills.slice(0, 6).forEach(s => {
            const card = document.createElement("div");
            card.className = "rec-card";
            const isHigh = s.priority === "High";
            card.innerHTML = `
                <div class="rec-card-header">
                    <div>
                        <div class="rec-category">${escapeHtml(s.category)}</div>
                        <div class="rec-skill-name">${escapeHtml(s.name)}</div>
                    </div>
                    <span class="rec-priority-badge ${isHigh ? 'priority-high' : 'priority-medium'}">
                        ${s.priority} Priority
                    </span>
                </div>
                <p class="rec-desc">${escapeHtml(s.description)}</p>
                <div class="rec-meta">
                    <div class="rec-meta-item">
                        <i class="fa-regular fa-clock"></i>
                        <span>~${s.duration_weeks || 2} wks</span>
                    </div>
                    <div class="rec-meta-item">
                        <i class="fa-solid fa-layer-group"></i>
                        <span>${escapeHtml(s.difficulty || 'Intermediate')}</span>
                    </div>
                </div>
                <div>
                    <span class="rec-resource-link">
                        <i class="fa-solid fa-graduation-cap"></i> ${escapeHtml(s.resource || 'Online documentation')}
                    </span>
                </div>
            `;
            recommendationCardsGrid.appendChild(card);
        });
    }

    function renderRoadmap(phases, estimatedTimeText) {
        roadmapTimeline.innerHTML = "";
        roadmapDurationText.textContent = estimatedTimeText;

        if (!phases || phases.length === 0) {
            roadmapTimeline.innerHTML = `<p class="empty-chip-state">No roadmap needed! Ready for applications.</p>`;
            return;
        }

        phases.forEach(phase => {
            const phaseEl = document.createElement("div");
            phaseEl.className = "phase-item";

            // Skills pills
            const skillsHtml = (phase.skills || []).map(skillName => 
                `<span class="phase-skill-pill"><i class="fa-solid fa-code"></i> ${escapeHtml(skillName)}</span>`
            ).join("");

            // Action items
            const actionItemsHtml = (phase.action_items || []).map(item => 
                `<li class="phase-action-item"><i class="fa-solid fa-circle-check"></i> <span>${escapeHtml(item)}</span></li>`
            ).join("");

            // Resources
            const resourcesHtml = (phase.resources || []).map(res => {
                const title = res.name || "Resource";
                const info = res.info || res.url || "";
                return `<span class="phase-res-item"><i class="fa-solid fa-book-open"></i> ${escapeHtml(title)}</span>`;
            }).join("");

            phaseEl.innerHTML = `
                <div class="phase-marker">
                    <div class="phase-marker-inner"></div>
                </div>
                <div class="phase-content-card">
                    <div class="phase-top">
                        <h4 class="phase-heading">${escapeHtml(phase.title)}</h4>
                        <span class="phase-duration-pill"><i class="fa-regular fa-clock"></i> ${escapeHtml(phase.duration)}</span>
                    </div>
                    <p class="phase-focus">${escapeHtml(phase.focus)}</p>
                    
                    ${skillsHtml ? `<div class="phase-skills-tags">${skillsHtml}</div>` : ''}

                    <ul class="phase-action-list">
                        ${actionItemsHtml}
                    </ul>

                    ${phase.capstone_project ? `
                        <div class="phase-project-box">
                            <i class="fa-solid fa-lightbulb"></i>
                            <div>
                                <strong>Hands-on Project Task:</strong> ${escapeHtml(phase.capstone_project)}
                            </div>
                        </div>
                    ` : ''}

                    ${resourcesHtml ? `
                        <div class="phase-resources">
                            <span class="phase-res-title">Curated Guides:</span>
                            ${resourcesHtml}
                        </div>
                    ` : ''}
                </div>
            `;
            roadmapTimeline.appendChild(phaseEl);
        });
    }

    // ==========================================
    // 6. Utility Functions & Export
    // ==========================================

    function animateCounter(element, target, suffix = "") {
        let current = 0;
        const duration = 1200;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            current = Math.round(easeOut * target);
            element.textContent = `${current}${suffix}`;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = `${target}${suffix}`;
            }
        }

        requestAnimationFrame(update);
    }

    function escapeHtml(str) {
        if (!str) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Reset All
    resetBtn.addEventListener("click", () => {
        userSkills = [];
        renderTags();
        jobDescriptionInput.value = "";
        updateCharCounter();
        resultsSection.style.display = "none";
        hideAlert();
        presetButtons.forEach(b => b.classList.remove("active"));
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // Print / PDF Export
    printRoadmapBtn.addEventListener("click", () => {
        window.print();
    });

    // Copy Summary to Clipboard
    copySummaryBtn.addEventListener("click", () => {
        if (!lastAnalysisData) return;

        const summaryText = `SkillBridge AI Career Gap Report
----------------------------------------
Match Score: ${lastAnalysisData.match_percentage}% (${lastAnalysisData.readiness_status})
Matched Skills (${lastAnalysisData.matched_count}): ${lastAnalysisData.matched_skills.map(s => s.name).join(", ") || "None"}
Skills to Learn (${lastAnalysisData.missing_count}): ${lastAnalysisData.missing_skills.map(s => s.name).join(", ") || "None"}
Estimated Roadmap Duration: ${lastAnalysisData.estimated_time_text}

Phased Roadmap:
${lastAnalysisData.roadmap.map(p => `• ${p.title} (${p.duration}): ${p.focus}`).join("\n")}
----------------------------------------
Generated by SkillBridge AI`;

        navigator.clipboard.writeText(summaryText).then(() => {
            const origText = copySummaryBtn.innerHTML;
            copySummaryBtn.innerHTML = `<i class="fa-solid fa-check"></i> Copied to Clipboard!`;
            setTimeout(() => {
                copySummaryBtn.innerHTML = origText;
            }, 2500);
        }).catch(err => {
            console.error("Clipboard copy failed:", err);
        });
    });

    // Initial render
    renderTags();
    updateCharCounter();

    // Auto-load first sample role if job description is empty for great first impression
    if (sampleRoles.length > 0 && !jobDescriptionInput.value.trim()) {
        loadPresetRole(sampleRoles[0]);
    }
});
