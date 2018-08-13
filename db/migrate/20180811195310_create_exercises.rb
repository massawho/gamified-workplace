class CreateExercises < ActiveRecord::Migration[5.2]
  def change
    create_table :exercises do |t|
      t.string :description
      t.date :due_at
      t.references :goal, foreign_key: true

      t.timestamps
    end
  end
end
