const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://lpbk52uyspqot6qucbffi2vzri0imjqt.lambda-url.ap-south-1.on.aws';

async function apiRequest(path: string, options: RequestInit = {}) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(error.message || error.detail || `API Error ${res.status}`);
  }
  return res.json();
}

// ──── Schemes ────
export async function listSchemes(params?: { category?: string; state?: string; search?: string; limit?: number }) {
  const query = new URLSearchParams();
  if (params?.category) query.set('category', params.category);
  if (params?.state) query.set('state', params.state);
  if (params?.search) query.set('search', params.search);
  if (params?.limit) query.set('limit', String(params.limit));
  return apiRequest(`/api/schemes/?${query}`);
}

export async function getSchemeDetail(schemeId: string) {
  return apiRequest(`/api/schemes/${schemeId}`);
}

export async function matchSchemes(profile: {
  age: number; incomeBracket: string; occupation: string;
  state: string; category?: string; disability?: boolean; gender?: string;
}) {
  return apiRequest('/api/schemes/match', {
    method: 'POST',
    body: JSON.stringify({ category: 'General', ...profile }),
  });
}

export async function getApplyGuide(schemeId: string) {
  return apiRequest(`/api/schemes/${schemeId}/apply-guide`);
}

// ──── Documents ────
export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/api/documents/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

export async function askDocument(docId: string, query: string, language = 'en') {
  return apiRequest(`/api/documents/${docId}/ask`, {
    method: 'POST',
    body: JSON.stringify({ query, language }),
  });
}

// ──── Chat ────
export async function sendChatMessage(message: string, language = 'en') {
  return apiRequest('/api/chat/message', {
    method: 'POST',
    body: JSON.stringify({ message, language }),
  });
}

// ──── Auth ────
export async function registerUser(phone: string, name: string) {
  return apiRequest('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ phone, name }),
  });
}

export async function verifyOTP(phone: string, otp: string) {
  return apiRequest('/api/auth/verify-otp', {
    method: 'POST',
    body: JSON.stringify({ phone, otp }),
  });
}

// ──── Profile ────
export async function createProfile(profile: any) {
  return apiRequest('/api/profile/', {
    method: 'POST',
    body: JSON.stringify(profile),
  });
}

export async function getProfile(userId: string) {
  return apiRequest(`/api/profile/${userId}`);
}

// ──── Stats ────
export async function getStats() {
  return apiRequest('/api/stats');
}
