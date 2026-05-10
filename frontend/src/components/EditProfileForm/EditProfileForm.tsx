import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api";
import "./EditProfileForm.scss";

interface InitialProfileData {
  bio?: string;
  website?: string;
  profile_pic?: string | null;
}

function EditProfileForm({ initialData }: { initialData: InitialProfileData }) {
  const navigate = useNavigate();
  const [bio, setBio] = useState(initialData.bio || "");
  const [website, setWebsite] = useState(initialData.website || "");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>(
    initialData.profile_pic || "https://via.placeholder.com/150",
  );

  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    const formData = new FormData();
    formData.append("bio", bio);
    formData.append("website", website);
    if (imageFile) formData.append("profile_pic", imageFile);

    try {
      await api.patch("/profile/update/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      navigate("/profile");
    } catch (err: any) {
      if (err.response?.data) setErrors(err.response.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="edit-profile-form" onSubmit={handleSubmit}>
      {errors.detail && <p className="global-error">{errors.detail[0]}</p>}

      <div className="picture-edit-section">
        <div className="preview-container">
          <img
            src={previewUrl}
            alt="Profile Preview"
            className="preview-image"
          />
        </div>
        <div className="upload-controls">
          <label htmlFor="profile-upload" className="btn-upload">
            Choose New Picture
          </label>
          <input
            id="profile-upload"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="hidden-input"
          />
          {errors.profile_pic && (
            <span className="error-text block mt-1">
              {errors.profile_pic[0]}
            </span>
          )}
        </div>
      </div>

      <div className="input-group">
        <label>Website</label>
        <input
          type="url"
          value={website}
          onChange={(e) => setWebsite(e.target.value)}
          className={`form-input ${errors.website ? "input-error" : ""}`}
          placeholder="https://yourwebsite.com"
        />
        {errors.website && (
          <span className="error-text">{errors.website[0]}</span>
        )}
      </div>

      <div className="input-group">
        <label>Bio</label>
        <textarea
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          className={`form-input ${errors.bio ? "input-error" : ""}`}
          placeholder="Tell people about yourself..."
          rows={4}
        />
        {errors.bio && <span className="error-text">{errors.bio[0]}</span>}
      </div>

      <div className="form-actions">
        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? "Saving..." : "Save Profile"}
        </button>
      </div>
    </form>
  );
}

export default EditProfileForm;
