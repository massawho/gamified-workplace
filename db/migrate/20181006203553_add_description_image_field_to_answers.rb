class AddDescriptionImageFieldToAnswers < ActiveRecord::Migration[5.2]
  def change
    add_column :answers, :description_image, :string
  end
end
