const API_BASE_URL = "http://localhost:8000";

export async function checkBackendHealth() {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
        throw new Error("Backend health check failed");
    }

    return response.json();
}

export interface ResearchProject {
    id: number;
    title: string;
    question: string;
    depth: string;
    sources: string;
    status: string;
    created_at: string;
    updated_at: string;
}

export interface CreateResearchProject {
    title: string;
    question: string;
    depth: string;
    sources: string;
}

export async function createResearchProject(
    project: CreateResearchProject
): Promise<ResearchProject> {
    const response = await fetch(`${API_BASE_URL}/api/research/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(project),
    });

    if (!response.ok) {
        throw new Error("Failed to create research project");
    }

    return response.json();
}

export async function getResearchProjects(): Promise<ResearchProject[]> {
    const response = await fetch(`${API_BASE_URL}/api/research/`);

    if (!response.ok) {
        throw new Error("Failed to fetch research projects");
    }

    return response.json();
}