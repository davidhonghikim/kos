import React, { useEffect, useState } from 'react'
import { getUsers, updateRole } from './admin-api'

export const AuthUsers = () => {
  const [users, setUsers] = useState([])

  useEffect(() => {
    getUsers().then(setUsers)
  }, [])

  const handleRoleChange = (id: string, role: string) => {
    updateRole(id, role).then(() => getUsers().then(setUsers))
  }

  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">User Management</h2>
      <table className="table-auto w-full">
        <thead>
          <tr><th>Email</th><th>Role</th><th>Change</th></tr>
        </thead>
        <tbody>
          {users.map((u: any) => (
            <tr key={u.id}>
              <td>{u.email}</td>
              <td>{u.role}</td>
              <td>
                <select value={u.role} onChange={(e) => handleRoleChange(u.id, e.target.value)}>
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                  <option value="dev">Dev</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
} 