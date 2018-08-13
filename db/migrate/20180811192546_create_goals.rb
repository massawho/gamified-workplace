class CreateGoals < ActiveRecord::Migration[5.2]
  def change
    create_table :goals do |t|
      t.string :description
      t.integer :money
      t.integer :frequency
      t.date :starts_at
      t.date :ends_at
      t.integer :level
      t.boolean :is_active

      t.timestamps
    end
  end
end
