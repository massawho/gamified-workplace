class CreateAnswers < ActiveRecord::Migration[5.2]
  def change
    create_table :answers do |t|
      t.text :description
      t.integer :answer_type
      t.string :upload
      t.text :extensive_answer
      t.references :assignment_deliverable, foreign_key: true

      t.timestamps
    end
  end
end
