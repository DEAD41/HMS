import { FormEvent, useEffect, useState } from 'react'
import { api, AuthUser, DemoUser, Facility, Patient } from './api'

const newId = () => crypto.randomUUID()

type Tab = 'ops' | 'mis' | 'ess'

export default function App() {
  const [health, setHealth] = useState('Checking')
  const [facilities, setFacilities] = useState<Facility[]>([])
  const [patients, setPatients] = useState<Patient[]>([])
  const [facilityId, setFacilityId] = useState('')
  const [selectedPatientId, setSelectedPatientId] = useState('')
  const [message, setMessage] = useState('Ready')
  const [user, setUser] = useState<AuthUser | null>(() => {
    const raw = localStorage.getItem('hms_user')
    return raw ? JSON.parse(raw) as AuthUser : null
  })
  const [demoUsers, setDemoUsers] = useState<DemoUser[]>([])
  const [tab, setTab] = useState<Tab>('ops')
  const [mis, setMis] = useState<Record<string, unknown> | null>(null)
  const [ess, setEss] = useState<Record<string, unknown> | null>(null)

  const refreshFacilities = async () => {
    const result = await api.listFacilities()
    setFacilities(result)
    if (!facilityId && result[0]) setFacilityId(result[0].id)
  }

  const refreshPatients = async (id = facilityId) => {
    if (!id) return
    const result = await api.searchPatients(id)
    setPatients(result)
    if (!selectedPatientId && result[0]) setSelectedPatientId(result[0].id)
  }

  useEffect(() => {
    api.health().then(x => setHealth(x.status)).catch(() => setHealth('Unavailable'))
    api.demoUsers().then(setDemoUsers).catch(() => undefined)
    refreshFacilities().catch(error => setMessage(error.message))
  }, [])

  useEffect(() => {
    refreshPatients().catch(error => setMessage(error.message))
  }, [facilityId])

  const login = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    try {
      const result = await api.login(String(data.get('userName')), String(data.get('password')))
      localStorage.setItem('hms_token', result.accessToken)
      localStorage.setItem('hms_user', JSON.stringify(result.user))
      setUser(result.user)
      setMessage(`Signed in as ${result.user.displayName}`)
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  const logout = () => {
    localStorage.removeItem('hms_token')
    localStorage.removeItem('hms_user')
    setUser(null)
    setEss(null)
    setMessage('Signed out')
  }

  const createFacility = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    try {
      const facility = await api.createFacility({
        code: String(data.get('code')),
        name: String(data.get('name')),
        timezone: String(data.get('timezone')),
        currency: String(data.get('currency')),
      })
      setFacilityId(facility.id)
      await refreshFacilities()
      setMessage(`Facility ${facility.code} created`)
      event.currentTarget.reset()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  const registerPatient = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    try {
      const patient = await api.registerPatient({
        facilityId,
        mrn: String(data.get('mrn')),
        firstName: String(data.get('firstName')),
        lastName: String(data.get('lastName')),
        phone: String(data.get('phone') ?? ''),
      })
      setSelectedPatientId(patient.id)
      await refreshPatients()
      setMessage(`Patient ${patient.mrn} registered`)
      event.currentTarget.reset()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  const scheduleAppointment = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    const startsAt = new Date(String(data.get('startsAt')))
    const endsAt = new Date(startsAt.getTime() + 30 * 60_000)
    try {
      const appointment = await api.scheduleAppointment({
        facilityId,
        patientId: selectedPatientId,
        clinicianEmployeeId: String(data.get('clinicianId') || newId()),
        startsAt: startsAt.toISOString(),
        endsAt: endsAt.toISOString(),
        reason: String(data.get('reason') ?? ''),
      })
      setMessage(`Appointment scheduled: ${appointment.id}`)
      event.currentTarget.reset()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  const loadMis = async () => {
    if (!facilityId) return
    try {
      setMis(await api.misDashboard(facilityId))
      setMessage('MIS dashboard loaded')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  const loadEss = async () => {
    try {
      setEss(await api.essMe())
      setMessage('ESS profile loaded')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  if (!user) {
    return (
      <main className="app">
        <header>
          <div>
            <h1>Healthcare ERP</h1>
            <div className="muted">Sign in to the operational console</div>
          </div>
          <span className="badge">API: {health}</span>
        </header>

        <form className="card" onSubmit={login} style={{ maxWidth: 420 }}>
          <h2>Login</h2>
          <label>Username<input name="userName" required defaultValue="admin" /></label>
          <label>Password<input name="password" type="password" required defaultValue="Admin@123" /></label>
          <div className="row"><button type="submit">Sign in</button></div>
          <p className="muted">{message}</p>
        </form>

        <section className="card">
          <h2>Sample users</h2>
          <table>
            <thead><tr><th>User</th><th>Password</th><th>Roles</th></tr></thead>
            <tbody>
              {demoUsers.map(u => (
                <tr key={u.userName}>
                  <td>{u.userName}</td>
                  <td><code>{u.password}</code></td>
                  <td>{u.roles.join(', ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    )
  }

  return (
    <main className="app">
      <header>
        <div>
          <h1>Healthcare ERP</h1>
          <div className="muted">{user.displayName} · {user.roles.join(', ')}</div>
        </div>
        <div className="row">
          <span className="badge">API: {health}</span>
          <button type="button" className="secondary" onClick={logout}>Sign out</button>
        </div>
      </header>

      <section className="card">
        <div className="row">
          <button type="button" className={tab === 'ops' ? '' : 'secondary'} onClick={() => setTab('ops')}>Operations</button>
          <button type="button" className={tab === 'mis' ? '' : 'secondary'} onClick={() => { setTab('mis'); void loadMis() }}>MIS</button>
          <button type="button" className={tab === 'ess' ? '' : 'secondary'} onClick={() => { setTab('ess'); void loadEss() }}>Self-service</button>
        </div>
        <p className="muted">{message}</p>
      </section>

      {tab === 'ops' && (
        <div className="grid">
          <form className="card" onSubmit={createFacility}>
            <h2>1. Facility</h2>
            <label>Code<input name="code" required placeholder="MAIN" /></label>
            <label>Name<input name="name" required placeholder="Main Hospital" /></label>
            <label>Timezone<input name="timezone" required defaultValue="Asia/Karachi" /></label>
            <label>Currency<input name="currency" required defaultValue="PKR" maxLength={3} /></label>
            <div className="row"><button type="submit">Create facility</button></div>
            <label>
              Active facility
              <select value={facilityId} onChange={event => setFacilityId(event.target.value)}>
                <option value="">Select</option>
                {facilities.map(f => <option key={f.id} value={f.id}>{f.code} — {f.name}</option>)}
              </select>
            </label>
          </form>

          <form className="card" onSubmit={registerPatient}>
            <h2>2. Patient registration</h2>
            <label>MRN<input name="mrn" required placeholder="MRN-0001" /></label>
            <label>First name<input name="firstName" required /></label>
            <label>Last name<input name="lastName" required /></label>
            <label>Phone<input name="phone" /></label>
            <div className="row">
              <button type="submit" disabled={!facilityId}>Register patient</button>
            </div>
          </form>

          <form className="card" onSubmit={scheduleAppointment}>
            <h2>3. Appointment</h2>
            <label>
              Patient
              <select value={selectedPatientId} onChange={event => setSelectedPatientId(event.target.value)}>
                <option value="">Select</option>
                {patients.map(p => <option key={p.id} value={p.id}>{p.mrn} — {p.firstName} {p.lastName}</option>)}
              </select>
            </label>
            <label>Clinician employee ID<input name="clinicianId" defaultValue={user.employeeId ?? newId()} required /></label>
            <label>Starts at<input name="startsAt" type="datetime-local" required /></label>
            <label>Reason<input name="reason" /></label>
            <div className="row">
              <button type="submit" disabled={!selectedPatientId}>Schedule</button>
            </div>
          </form>
        </div>
      )}

      {tab === 'mis' && (
        <section className="card">
          <h2>MIS dashboard</h2>
          <div className="row">
            <button type="button" onClick={() => void loadMis()} disabled={!facilityId}>Refresh</button>
          </div>
          <pre>{mis ? JSON.stringify(mis, null, 2) : 'Select a facility and refresh.'}</pre>
        </section>
      )}

      {tab === 'ess' && (
        <section className="card">
          <h2>Employee self-service</h2>
          <p className="muted">Requires the signed-in user to be linked to an HRIS employee (Admin/Hr can link).</p>
          <div className="row">
            <button type="button" onClick={() => void loadEss()}>Refresh my profile</button>
          </div>
          <pre>{ess ? JSON.stringify(ess, null, 2) : 'No ESS data yet.'}</pre>
        </section>
      )}
    </main>
  )
}
