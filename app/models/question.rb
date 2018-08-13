class Question < ApplicationRecord

  validates :answer_type, :description, presence: true

  ANSWER_TYPE_UPLOAD = 1
  ANSWER_TYPE_TEXT = 2

  def upload?
    self.answer_type == Question::ANSWER_TYPE_UPLOAD
  end

  def generate_answer
    answer = Answer.new
    answer.answer_type = self.answer_type
    answer.description = self.description
    answer
  end

end
