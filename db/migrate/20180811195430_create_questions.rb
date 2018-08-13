class CreateQuestions < ActiveRecord::Migration[5.2]
  def change
    create_table :questions do |t|
      t.text :description
      t.integer :answer_type
      t.references :exercise, foreign_key: true

      t.timestamps
    end
  end
end
