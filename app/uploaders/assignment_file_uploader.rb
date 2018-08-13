class AssignmentFileUploader < CarrierWave::Uploader::Base

  storage :file

  def store_dir
    "/private/assignments/#{model.assignment_deliverable.id}"
  end

  def extension_whitelist
    %w(cs docx doc pdf rb c)
  end
end
