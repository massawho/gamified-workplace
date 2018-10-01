class AddFeedbackFieldToAnswers < ActiveRecord::Migration[5.2]
  def change
    add_column :answers, :feedback, :text
  end
end
