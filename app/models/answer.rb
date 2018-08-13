class Answer < ApplicationRecord
  belongs_to :assignment_deliverable

  mount_uploader :upload, AssignmentFileUploader

  def upload?
    self.answer_type.to_i == Question::ANSWER_TYPE_UPLOAD
  end
end
