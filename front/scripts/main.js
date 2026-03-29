(function () {
    const API_BASE_URL = "http://127.0.0.1:8000/api/convert";
    const POLL_INTERVAL_MS = 1800;

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
        pollingHandle: null,
    };

    function getSelectedTool() {
        return window.CONVERTER_CONFIGS.find((tool) => tool.id === appState.selectedToolId);
    }

    function createToolCardMarkup(tool) {
        return `
            <article class="tool-card" data-tool-id="${tool.id}">
                <div class="tool-card-top">
                    <div class="tool-badge"><span>${tool.badge}</span></div>
                    <span class="tool-arrow">↗</span>
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

            if (!payload.task_id) {
                throw new Error("Task id was not returned by the backend.");
            }

            progressMessage.textContent = "Upload accepted. Waiting for the conversion worker to finish.";
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
        if (!appState.resultFilename) {
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/download/${appState.resultFilename}/`);
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
        } catch (error) {
            showError("Download failed", error.message);
        }
    }

    function showError(title, message) {
        errorTitle.textContent = title;
        errorMessage.textContent = message;
        setStage("error");
    }

    function resetWorkspace() {
        appState.selectedFile = null;
        appState.resultFilename = "";
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
    }

    boot();
})();
