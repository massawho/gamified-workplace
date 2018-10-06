class Question < ApplicationRecord

  validates :answer_type, :description, :file_name, presence: true
  mount_uploader :description_image, QuestionFileUploader

  ANSWER_TYPE_UPLOAD = 1
  ANSWER_TYPE_TEXT = 2

  def upload?
    self.answer_type == Question::ANSWER_TYPE_UPLOAD
  end

  def generate_answer
    answer = Answer.new
    answer.answer_type = self.answer_type
    answer.description = self.description
    answer.description_image = self.description_image
    answer.file_name = self.file_name
    answer
  end

end
