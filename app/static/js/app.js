/**
 * Global Alpine.js application logic & helper scripts for Enterprise UI
 */

document.addEventListener('alpine:init', () => {
    // Global Toast Notification Store
    Alpine.store('toast', {
        toasts: [],
        show(message, type = 'success') {
            const id = Date.now();
            this.toasts.push({ id, message, type });
            setTimeout(() => {
                this.remove(id);
            }, 4000);
        },
        remove(id) {
            this.toasts = this.toasts.filter(t => t.id !== id);
        }
    });

    // Enterprise App State Manager (Sidebar + Theme)
    Alpine.data('enterpriseLayout', () => ({
        sidebarOpen: true,
        theme: localStorage.getItem('theme') || 'dark',
        
        init() {
            this.applyTheme();
        },

        toggleSidebar() {
            this.sidebarOpen = !this.sidebarOpen;
        },

        toggleTheme() {
            this.theme = this.theme === 'dark' ? 'light' : 'dark';
            localStorage.setItem('theme', this.theme);
            this.applyTheme();
            
            // Dispatch event for charts to adapt
            window.dispatchEvent(new CustomEvent('theme-changed', { detail: { theme: this.theme } }));
            
            // Sync with backend API
            fetch('/api/v1/user/settings', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ theme: this.theme })
            }).catch(() => {});
        },

        applyTheme() {
            if (this.theme === 'dark') {
                document.documentElement.classList.add('dark');
                document.documentElement.classList.remove('light');
            } else {
                document.documentElement.classList.remove('dark');
                document.documentElement.classList.add('light');
            }
        }
    }));

    // Drag and Drop File Uploader Component
    Alpine.data('fileUploader', () => ({
        isDragging: false,
        file: null,
        uploading: false,
        progress: 0,
        errorMessage: '',

        handleDrop(e) {
            this.isDragging = false;
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.validateAndSetFile(files[0]);
            }
        },

        handleFileSelect(e) {
            const files = e.target.files;
            if (files.length > 0) {
                this.validateAndSetFile(files[0]);
            }
        },

        validateAndSetFile(file) {
            this.errorMessage = '';
            const ext = file.name.split('.').pop().toLowerCase();
            if (!['pdf', 'docx'].includes(ext)) {
                this.errorMessage = 'Invalid file format. Please select a PDF or DOCX file.';
                Alpine.store('toast').show(this.errorMessage, 'error');
                return;
            }
            if (file.size > 10 * 1024 * 1024) {
                this.errorMessage = 'File size exceeds maximum limit of 10MB.';
                Alpine.store('toast').show(this.errorMessage, 'error');
                return;
            }
            this.file = file;
        },

        async submitUpload() {
            if (!this.file) return;
            this.uploading = true;
            this.progress = 25;

            const formData = new FormData();
            formData.append('file', this.file);

            try {
                this.progress = 60;
                const res = await fetch('/api/v1/resumes/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await res.json();
                this.progress = 100;
                
                if (!res.ok) {
                    throw new Error(data.detail || 'Upload failed');
                }

                Alpine.store('toast').show('Resume uploaded & parsed successfully!', 'success');

                // Trigger ATS Analysis directly
                const analysisRes = await fetch('/api/v1/analysis/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ resume_id: data.id })
                });

                const analysisData = await analysisRes.json();
                if (analysisRes.ok) {
                    setTimeout(() => {
                        window.location.href = `/analysis/${analysisData.id}`;
                    }, 800);
                } else {
                    window.location.href = '/dashboard';
                }
            } catch (err) {
                this.uploading = false;
                this.errorMessage = err.message;
                Alpine.store('toast').show(err.message, 'error');
            }
        }
    }));

    // Job Matcher Component
    Alpine.data('jobMatcher', () => ({
        selectedResumeId: '',
        jobTitle: '',
        jobDescription: '',
        analyzing: false,

        async runMatching() {
            if (!this.selectedResumeId) {
                Alpine.store('toast').show('Please select a resume from your history.', 'error');
                return;
            }
            if (!this.jobDescription.trim()) {
                Alpine.store('toast').show('Please paste target job description requirements.', 'error');
                return;
            }

            this.analyzing = true;
            try {
                const res = await fetch('/api/v1/analysis/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        resume_id: parseInt(this.selectedResumeId),
                        job_title: this.jobTitle || 'Target Position',
                        job_description: this.jobDescription
                    })
                });

                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || 'Job matching analysis failed');
                }

                Alpine.store('toast').show('Job Match analysis completed!', 'success');
                window.location.href = `/analysis/${data.id}`;
            } catch (err) {
                this.analyzing = false;
                Alpine.store('toast').show(err.message, 'error');
            }
        }
    }));
});
