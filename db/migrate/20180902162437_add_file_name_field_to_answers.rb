class AddFileNameFieldToAnswers < ActiveRecord::Migration[5.2]
  def change
    add_column :answers, :file_name, :string
  end
end
