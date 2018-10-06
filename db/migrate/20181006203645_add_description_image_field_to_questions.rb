class AddDescriptionImageFieldToQuestions < ActiveRecord::Migration[5.2]
  def change
    add_column :questions, :description_image, :string
  end
end
