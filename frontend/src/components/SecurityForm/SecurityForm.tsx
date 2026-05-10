import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api";
// We will reuse the same SCSS styles since the layout is identical!
import "../EditProfileForm/EditProfileForm.scss";

interface InitialSecurityData {
  first_name?: string;
  last_name?: string;
  username?: string;
  email?: string;
}

function SecurityForm({ initialData }: { initialData: InitialSecurityData }) {
  const navigate = useNavigate();

  const [firstName, setFirstName] = useState(initialData.first_name || "");
  const [lastName, setLastName] = useState(initialData.last_name || "");
  const [username, setUsername] = useState(initialData.username || "");
  const [email, setEmail] = useState(initialData.email || "");
  const [password, setPassword] = useState(""); // Leave blank by default
  const [confirmPassword, setConfirmPassword] = useState(""); // 👈 1. ADD THIS

  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string[]>>({});
  const [successMsg, setSuccessMsg] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});
    setSuccessMsg("");

    // Package the data. We ONLY send the password if they actually typed a new one.
    const payload: any = {
      first_name: firstName,
      last_name: lastName,
      username: username,
      email: email,
    };

    // 👈 2. REPLACE THE EXISTING PASSWORD CHECK WITH THIS:
    if (password.trim() !== "") {
      if (password !== confirmPassword) {
        setErrors({ confirm_password: ["Passwords do not match."] });
        setLoading(false);
        return;
      }
      payload.password = password;
      payload.confirm_password = confirmPassword;
    }

    try {
      await api.patch("/security/update/", payload);
      setSuccessMsg("Security information updated successfully!");
      setPassword(""); // Clear the password field
      setConfirmPassword(""); // 👈 3. ADD THIS
    } catch (err: any) {
      if (err.response?.data) setErrors(err.response.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="edit-profile-form" onSubmit={handleSubmit}>
      {errors.detail && <p className="global-error">{errors.detail[0]}</p>}
      {successMsg && (
        <p
          className="global-error"
          style={{ backgroundColor: "#d4edda", color: "#155724" }}
        >
          {successMsg}
        </p>
      )}

      <div className="name-row">
        <div className="input-group">
          <label>First Name</label>
          <input
            type="text"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            className={`form-input ${errors.first_name ? "input-error" : ""}`}
          />
          {errors.first_name && (
            <span className="error-text">{errors.first_name[0]}</span>
          )}
        </div>

        <div className="input-group">
          <label>Last Name</label>
          <input
            type="text"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            className={`form-input ${errors.last_name ? "input-error" : ""}`}
          />
          {errors.last_name && (
            <span className="error-text">{errors.last_name[0]}</span>
          )}
        </div>
      </div>

      <div className="input-group">
        <label>Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className={`form-input ${errors.username ? "input-error" : ""}`}
        />
        {errors.username && (
          <span className="error-text">{errors.username[0]}</span>
        )}
      </div>

      <div className="input-group">
        <label>Email Address</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={`form-input ${errors.email ? "input-error" : ""}`}
        />
        {errors.email && <span className="error-text">{errors.email[0]}</span>}
      </div>

      <hr
        style={{
          border: "none",
          borderTop: "1px solid #eee",
          margin: "15px 0",
        }}
      />

      <div className="input-group">
        <label>Change Password (leave blank to keep current)</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={`form-input ${errors.password ? "input-error" : ""}`}
          placeholder="New Password"
        />
        {errors.password && (
          <span className="error-text">{errors.password[0]}</span>
        )}
      </div>

      {/* 👈 4. ADD THIS NEW CONFIRM FIELD RIGHT BELOW THE EXISTING PASSWORD FIELD */}
      <div className="input-group">
        <label>Confirm New Password</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          className={`form-input ${errors.confirm_password ? "input-error" : ""}`}
          placeholder="Confirm New Password"
        />
        {errors.confirm_password && (
          <span className="error-text">{errors.confirm_password[0]}</span>
        )}
      </div>

      <div className="form-actions">
        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? "Saving..." : "Update Security Settings"}
        </button>
      </div>
    </form>
  );
}

export default SecurityForm;
