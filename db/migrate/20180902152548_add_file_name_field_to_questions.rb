class AddFileNameFieldToQuestions < ActiveRecord::Migration[5.2]
  def change
    add_column :questions, :file_name, :string
  end
end
