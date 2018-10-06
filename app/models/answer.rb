class Answer < ApplicationRecord
  belongs_to :assignment_deliverable

  mount_uploader :upload, AssignmentFileUploader
  mount_uploader :description_image, QuestionFileUploader

  def upload?
    self.answer_type.to_i == Question::ANSWER_TYPE_UPLOAD
  end
end
