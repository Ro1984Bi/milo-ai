

export default function Logout() {
    const handleLogout = () => {
        localStorage.removeItem('token')
        window.location.href = '/login'
    }
    return (
        <button className="btn btn-ghost text-lg text-white px-4 py-2 rounded" onClick={handleLogout}>
            Logout
        </button>
    )
}
