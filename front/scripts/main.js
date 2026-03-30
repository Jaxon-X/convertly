(function () {
    const API_BASE_URL = "http://127.0.0.1:8000/api/convert";
    const AUTH_API_BASE_URL = "http://127.0.0.1:8000/api/user";
    const POLL_INTERVAL_MS = 1800;
    const AUTH_STORAGE_KEY = "convertlyAuth";

    const toolGrid = document.getElementById("toolGrid");
    const miniToolGrid = document.getElementById("miniToolGrid");
    const fileInput = document.getElementById("fileInput");
    const dropZone = document.getElementById("dropZone");
    const converterStage = document.getElementById("converterStage");
    const uploadStage = document.getElementById("uploadStage");
    const fileStage = document.getElementById("fileStage");
    const progressStage = document.getElementById("progressStage");
    const resultStage = document.getElementById("resultStage");
    const errorStage = document.getElementById("errorStage");
    const convertButton = document.getElementById("convertButton");
    const resetFileButton = document.getElementById("resetFileButton");
    const changeFileButton = document.getElementById("changeFileButton");
    const retryButton = document.getElementById("retryButton");
    const clearErrorButton = document.getElementById("clearErrorButton");
    const downloadButton = document.getElementById("downloadButton");
    const convertAnotherButton = document.getElementById("convertAnotherButton");
    const switcherToggle = document.getElementById("switcherToggle");

    const toolTitle = document.getElementById("toolTitle");
    const toolDescription = document.getElementById("toolDescription");
    const toolAccept = document.getElementById("toolAccept");
    const toolOutput = document.getElementById("toolOutput");
    const workspaceHeading = document.getElementById("workspaceHeading");
    const dropHint = document.getElementById("dropHint");
    const selectedFileBadge = document.getElementById("selectedFileBadge");
    const selectedFileName = document.getElementById("selectedFileName");
    const selectedFileMeta = document.getElementById("selectedFileMeta");
    const progressTitle = document.getElementById("progressTitle");
    const progressMessage = document.getElementById("progressMessage");
    const resultTitle = document.getElementById("resultTitle");
    const resultFilename = document.getElementById("resultFilename");
    const errorTitle = document.getElementById("errorTitle");
    const errorMessage = document.getElementById("errorMessage");

    const authButton = document.getElementById("authButton");
    const userChip = document.getElementById("userChip");
    const userChipName = document.getElementById("userChipName");
    const authModalBackdrop = document.getElementById("authModalBackdrop");
    const authModalClose = document.getElementById("authModalClose");
    const loginTab = document.getElementById("loginTab");
    const registerTab = document.getElementById("registerTab");
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const authFeedback = document.getElementById("authFeedback");
    const loginEmailInput = document.getElementById("loginEmail");
    const loginPasswordInput = document.getElementById("loginPassword");
    const registerEmailInput = document.getElementById("registerEmail");
    const registerPasswordInput = document.getElementById("registerPassword");

    const stageElements = {
        idle: uploadStage,
        selected: fileStage,
        converting: progressStage,
        success: resultStage,
        error: errorStage,
    };

    const appState = {
        selectedToolId: window.CONVERTER_CONFIGS[0].id,
        selectedFile: null,
        resultFilename: "",
        downloadToken: "",
        pollingHandle: null,
        pendingDownloadAfterAuth: false,
        authMode: "login",
    };

    function getSelectedTool() {
        return window.CONVERTER_CONFIGS.find((tool) => tool.id === appState.selectedToolId);
    }

    function getStoredAuth() {
        const raw = localStorage.getItem(AUTH_STORAGE_KEY);
        return raw ? JSON.parse(raw) : null;
    }

    function setStoredAuth(payload) {
        localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(payload));
    }

    function clearStoredAuth() {
        localStorage.removeItem(AUTH_STORAGE_KEY);
    }

    function isAuthenticated() {
        const auth = getStoredAuth();
        return Boolean(auth && auth.access);
    }

    function createToolCardMarkup(tool) {
        return `
            <article class="tool-card tone-${tool.tone}" data-tool-id="${tool.id}">
                <div class="tool-card-top">
                    <div class="tool-badge tone-${tool.tone}"><span>${tool.badge}</span></div>
                    <span class="tool-arrow">&rarr;</span>
                </div>
                <h3>${tool.title}</h3>
                <p>${tool.description}</p>
            </article>
        `;
    }

    function renderToolCards() {
        const cardsMarkup = window.CONVERTER_CONFIGS.map((tool) => createToolCardMarkup(tool)).join("");
        toolGrid.innerHTML = cardsMarkup;
        miniToolGrid.innerHTML = cardsMarkup.replaceAll("tool-card", "mini-tool-card");

        document.querySelectorAll("[data-tool-id]").forEach((card) => {
            card.addEventListener("click", () => handleToolChange(card.dataset.toolId));
        });

        syncToolCardSelection();
    }

    function syncToolCardSelection() {
        document.querySelectorAll("[data-tool-id]").forEach((card) => {
            card.classList.toggle("is-active", card.dataset.toolId === appState.selectedToolId);
        });
    }

    function handleToolChange(toolId) {
        if (toolId === appState.selectedToolId) {
            return;
        }

        appState.selectedToolId = toolId;
        appState.selectedFile = null;
        appState.resultFilename = "";
        appState.downloadToken = "";
        clearPolling();
        syncToolCardSelection();
        hydrateTool();
        setStage("idle");
    }

    function hydrateTool() {
        const tool = getSelectedTool();
        toolTitle.textContent = tool.title;
        toolDescription.textContent = tool.description;
        toolAccept.textContent = tool.accept.join(", ");
        toolOutput.textContent = tool.outputLabel;
        workspaceHeading.textContent = tool.heading;
        dropHint.textContent = `Supports ${tool.accept.join(", ")} files up to 50MB.`;
        progressTitle.textContent = `Converting ${tool.shortLabel} into ${tool.outputLabel}`;
        selectedFileBadge.textContent = tool.badge;
        selectedFileBadge.className = `selected-file-icon tone-${tool.tone}`;
        fileInput.setAttribute("accept", tool.accept.join(","));
    }

    function setStage(stage) {
        converterStage.dataset.state = stage;

        Object.entries(stageElements).forEach(([stageName, element]) => {
            element.classList.toggle("stage-active", stageName === stage);
        });

        document.querySelectorAll(".timeline-item").forEach((item) => {
            const step = item.dataset.step;
            const isActive =
                (stage === "idle" && step === "select") ||
                (stage === "selected" && step === "select") ||
                (stage === "converting" && step === "convert") ||
                ((stage === "success" || stage === "error") && step === "download");
            item.classList.toggle("is-active", isActive);
        });
    }

    function handleDropEvents() {
        ["dragenter", "dragover"].forEach((eventName) => {
            dropZone.addEventListener(eventName, (event) => {
                event.preventDefault();
                dropZone.classList.add("drag-over");
            });
        });

        ["dragleave", "dragend"].forEach((eventName) => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove("drag-over");
            });
        });

        dropZone.addEventListener("drop", (event) => {
            event.preventDefault();
            dropZone.classList.remove("drag-over");
            const file = event.dataTransfer.files[0];
            if (file) {
                selectFile(file);
            }
        });
    }

    function validateFile(file, tool) {
        const extension = `.${file.name.split(".").pop().toLowerCase()}`;
        if (!tool.accept.includes(extension)) {
            return `This tool only accepts ${tool.accept.join(", ")} files.`;
        }

        if (file.size > 50 * 1024 * 1024) {
            return "Please upload a file smaller than 50MB.";
        }

        return "";
    }

    function selectFile(file) {
        const validationError = validateFile(file, getSelectedTool());
        if (validationError) {
            showError("Unsupported file", validationError);
            return;
        }

        appState.selectedFile = file;
        selectedFileName.textContent = file.name;
        selectedFileMeta.textContent = `${formatBytes(file.size)} ready for ${getSelectedTool().outputLabel} output`;
        setStage("selected");
    }

    async function handleConvert() {
        if (!appState.selectedFile) {
            showError("No file selected", "Choose a file before starting the conversion.");
            return;
        }

        const tool = getSelectedTool();
        const formData = new FormData();
        formData.append("file", appState.selectedFile);

        appState.downloadToken = "";
        setStage("converting");
        progressMessage.textContent = "Uploading the file and creating a worker task.";

        try {
            const response = await fetch(`${API_BASE_URL}${tool.endpoint}`, {
                method: "POST",
                body: formData,
            });

            const payload = await parseJson(response);
            if (!response.ok) {
                throw new Error(payload.error || payload.message || "The backend rejected the upload.");
            }

            if (!payload.task_id || !payload.download_token) {
                throw new Error("The backend response is incomplete for secure download.");
            }

            progressMessage.textContent = "Upload accepted. Waiting for the conversion worker to finish.";
            appState.downloadToken = payload.download_token;
            await pollTaskStatus(payload.task_id, payload.filename);
        } catch (error) {
            showError("Conversion failed", error.message);
        }
    }

    function pollTaskStatus(taskId, filename) {
        clearPolling();

        return new Promise((resolve, reject) => {
            const checkStatus = async () => {
                try {
                    const response = await fetch(`${API_BASE_URL}/status/${taskId}/`);
                    const payload = await parseJson(response);

                    if (!response.ok) {
                        throw new Error(payload.error || "Could not read the task status.");
                    }

                    if (payload.task_status === "SUCCESS") {
                        clearPolling();
                        appState.resultFilename = filename;
                        resultFilename.textContent = filename;
                        resultTitle.textContent = `${getSelectedTool().outputLabel} output is ready`;
                        setStage("success");
                        resolve();
                        return;
                    }

                    if (payload.task_status === "FAILURE") {
                        clearPolling();
                        reject(new Error("The backend worker reported a failed conversion."));
                    }
                } catch (error) {
                    clearPolling();
                    reject(error);
                }
            };

            appState.pollingHandle = window.setInterval(checkStatus, POLL_INTERVAL_MS);
            checkStatus();
        });
    }

    async function handleDownload() {
        if (!appState.resultFilename || !appState.downloadToken) {
            showError("Download unavailable", "Please convert a file again before downloading.");
            return;
        }

        if (!isAuthenticated()) {
            appState.pendingDownloadAfterAuth = true;
            openAuthModal("register", "Create a quick account to unlock the download.");
            return;
        }

        try {
            const auth = getStoredAuth();
            const response = await fetch(
                `${API_BASE_URL}/download/${appState.resultFilename}/?token=${encodeURIComponent(appState.downloadToken)}`,
                {
                    headers: {
                        Authorization: `Bearer ${auth.access}`,
                    },
                },
            );

            if (response.status === 401) {
                appState.pendingDownloadAfterAuth = true;
                clearStoredAuth();
                updateAuthUI();
                openAuthModal("login", "Your session expired. Please sign in again to continue the download.");
                return;
            }

            if (!response.ok) {
                const payload = await parseJson(response);
                throw new Error(payload.error || "Download could not be completed.");
            }

            const blob = await response.blob();
            const objectUrl = URL.createObjectURL(blob);
            const anchor = document.createElement("a");
            anchor.href = objectUrl;
            anchor.download = appState.resultFilename;
            document.body.appendChild(anchor);
            anchor.click();
            anchor.remove();
            URL.revokeObjectURL(objectUrl);
            appState.pendingDownloadAfterAuth = false;
        } catch (error) {
            showError("Download failed", error.message);
        }
    }

    async function handleLogout() {
        const auth = getStoredAuth();
        if (auth && auth.refresh) {
            try {
                await fetch(`${AUTH_API_BASE_URL}/logout/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${auth.access}`,
                    },
                    body: JSON.stringify({ refresh: auth.refresh }),
                });
            } catch (error) {
                console.error(error);
            }
        }

        clearStoredAuth();
        updateAuthUI();
    }

    function updateAuthUI() {
        const auth = getStoredAuth();
        if (auth && auth.access) {
            authButton.textContent = "Log out";
            userChip.hidden = false;
            userChipName.textContent = auth.username || auth.email;
        } else {
            authButton.textContent = "Sign In";
            userChip.hidden = true;
            userChipName.textContent = "Guest";
        }
    }

    function openAuthModal(mode, feedbackMessage = "") {
        appState.authMode = mode;
        authModalBackdrop.hidden = false;
        switchAuthMode(mode);
        if (feedbackMessage) {
            setAuthFeedback(feedbackMessage, false);
        } else {
            hideAuthFeedback();
        }
    }

    function closeAuthModal() {
        authModalBackdrop.hidden = true;
        hideAuthFeedback();
    }

    function switchAuthMode(mode) {
        appState.authMode = mode;
        const isLogin = mode === "login";
        loginTab.classList.toggle("is-active", isLogin);
        registerTab.classList.toggle("is-active", !isLogin);
        loginForm.classList.toggle("auth-form-active", isLogin);
        registerForm.classList.toggle("auth-form-active", !isLogin);
    }

    function setAuthFeedback(message, isSuccess) {
        authFeedback.hidden = false;
        authFeedback.textContent = message;
        authFeedback.classList.toggle("is-success", isSuccess);
    }

    function hideAuthFeedback() {
        authFeedback.hidden = true;
        authFeedback.textContent = "";
        authFeedback.classList.remove("is-success");
    }

    async function handleAuthSubmit(event) {
        event.preventDefault();

        const form = event.currentTarget;
        const mode = form.id === "loginForm" ? "login" : "register";
        const endpoint = mode === "login" ? "/login/" : "/register/";
        const payload = Object.fromEntries(new FormData(form).entries());

        try {
            const response = await fetch(`${AUTH_API_BASE_URL}${endpoint}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            const data = await parseJson(response);
            if (!response.ok) {
                const firstError = extractErrorMessage(data);
                throw new Error(firstError || "Authentication failed.");
            }

            if (mode === "register") {
                switchAuthMode("login");
                loginEmailInput.value = registerEmailInput.value;
                loginPasswordInput.value = registerPasswordInput.value;
                registerForm.reset();
                setAuthFeedback(
                    "Registration successful. Now click 'Login and download' to continue.",
                    true,
                );
                return;
            }

            setStoredAuth({
                username: data.username,
                email: data.email,
                access: data.access,
                refresh: data.refresh,
                is_email_verified: data.is_email_verified,
            });

            updateAuthUI();
            setAuthFeedback("Login successful. Continuing your download.", true);

            window.setTimeout(async () => {
                closeAuthModal();
                if (appState.pendingDownloadAfterAuth) {
                    await handleDownload();
                }
            }, 450);
        } catch (error) {
            setAuthFeedback(error.message, false);
        }
    }

    function extractErrorMessage(payload) {
        if (!payload || typeof payload !== "object") {
            return "";
        }

        if (payload.error) {
            return payload.error;
        }

        const firstKey = Object.keys(payload)[0];
        if (!firstKey) {
            return "";
        }

        const value = payload[firstKey];
        if (Array.isArray(value)) {
            return value[0];
        }
        return value;
    }

    function showError(title, message) {
        errorTitle.textContent = title;
        errorMessage.textContent = message;
        setStage("error");
    }

    function resetWorkspace() {
        appState.selectedFile = null;
        appState.resultFilename = "";
        appState.downloadToken = "";
        appState.pendingDownloadAfterAuth = false;
        clearPolling();
        fileInput.value = "";
        hydrateTool();
        setStage("idle");
    }

    function clearPolling() {
        if (appState.pollingHandle) {
            clearInterval(appState.pollingHandle);
            appState.pollingHandle = null;
        }
    }

    function formatBytes(value) {
        if (value < 1024) {
            return `${value} B`;
        }
        if (value < 1024 * 1024) {
            return `${(value / 1024).toFixed(1)} KB`;
        }
        return `${(value / (1024 * 1024)).toFixed(1)} MB`;
    }

    async function parseJson(response) {
        const text = await response.text();
        return text ? JSON.parse(text) : {};
    }

    function boot() {
        renderToolCards();
        hydrateTool();
        updateAuthUI();
        setStage("idle");
        handleDropEvents();

        fileInput.addEventListener("change", (event) => {
            const file = event.target.files[0];
            if (file) {
                selectFile(file);
            }
        });

        convertButton.addEventListener("click", handleConvert);
        resetFileButton.addEventListener("click", resetWorkspace);
        changeFileButton.addEventListener("click", () => fileInput.click());
        convertAnotherButton.addEventListener("click", resetWorkspace);
        clearErrorButton.addEventListener("click", resetWorkspace);
        retryButton.addEventListener("click", () => {
            if (appState.selectedFile) {
                setStage("selected");
            } else {
                resetWorkspace();
            }
        });
        downloadButton.addEventListener("click", handleDownload);
        switcherToggle.addEventListener("click", () => {
            document.getElementById("tools").scrollIntoView({ behavior: "smooth", block: "start" });
        });

        authButton.addEventListener("click", () => {
            if (isAuthenticated()) {
                handleLogout();
            } else {
                openAuthModal("login");
            }
        });
        authModalClose.addEventListener("click", closeAuthModal);
        authModalBackdrop.addEventListener("click", (event) => {
            if (event.target === authModalBackdrop) {
                closeAuthModal();
            }
        });
        loginTab.addEventListener("click", () => switchAuthMode("login"));
        registerTab.addEventListener("click", () => switchAuthMode("register"));
        loginForm.addEventListener("submit", handleAuthSubmit);
        registerForm.addEventListener("submit", handleAuthSubmit);
    }

    boot();
})();
