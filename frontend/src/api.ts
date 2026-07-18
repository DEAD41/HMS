const API_BASE = import.meta.env.VITE_API_BASE ?? ''

function authHeaders(): HeadersInit {
  const token = localStorage.getItem('hms_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...(init?.headers ?? {}),
    },
    ...init,
  })

  const text = await response.text()
  const data = text ? JSON.parse(text) : null
  if (!response.ok) {
    throw new Error(data?.error ?? `Request failed (${response.status})`)
  }
  return data as T
}

export type Facility = {
  id: string
  code: string
  name: string
  timezone: string
  currency: string
  status: string
}

export type Patient = {
  id: string
  facilityId: string
  mrn: string
  firstName: string
  lastName: string
  status: string
}

export type Appointment = {
  id: string
  patientId: string
  clinicianEmployeeId: string
  startsAt: string
  endsAt: string
  status: string
}

export type AuthUser = {
  id: string
  userName: string
  displayName: string
  roles: string[]
  employeeId?: string | null
  defaultFacilityId?: string | null
}

export type LoginResponse = {
  accessToken: string
  tokenType: string
  user: AuthUser
}

export type DemoUser = {
  userName: string
  password: string
  roles: string[]
}

export const api = {
  health: () => request<{ status: string }>('/api/health'),
  demoUsers: () => request<DemoUser[]>('/api/fnd/auth/demo-users'),
  login: (userName: string, password: string) =>
    request<LoginResponse>('/api/fnd/auth/login', {
      method: 'POST',
      body: JSON.stringify({ userName, password }),
    }),
  me: () => request<AuthUser>('/api/fnd/auth/me'),
  listFacilities: () => request<Facility[]>('/api/fnd/facilities'),
  createFacility: (body: { code: string; name: string; timezone: string; currency: string }) =>
    request<Facility>('/api/fnd/facilities', { method: 'POST', body: JSON.stringify(body) }),
  searchPatients: (facilityId: string, query = '') =>
    request<Patient[]>(`/api/hms/patients?facilityId=${facilityId}&query=${encodeURIComponent(query)}`),
  registerPatient: (body: {
    facilityId: string
    mrn: string
    firstName: string
    lastName: string
    phone?: string
  }) => request<Patient>('/api/hms/patients', { method: 'POST', body: JSON.stringify(body) }),
  scheduleAppointment: (body: {
    facilityId: string
    patientId: string
    clinicianEmployeeId: string
    startsAt: string
    endsAt: string
    reason?: string
  }) => request<Appointment>('/api/hms/appointments', { method: 'POST', body: JSON.stringify(body) }),
  misDashboard: (facilityId: string) => request<Record<string, unknown>>(`/api/fin/mis/dashboard?facilityId=${facilityId}`),
  essMe: () => request<Record<string, unknown>>('/api/hris/ess/me'),
  listScorecards: (facilityId: string) => request<unknown[]>(`/api/prc/scorecards?facilityId=${facilityId}`),
  listBudgets: (facilityId: string) => request<unknown[]>(`/api/fin/budgets?facilityId=${facilityId}`),
}
