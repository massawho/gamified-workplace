class CreateAchievedBadges < ActiveRecord::Migration[5.2]
  def change
    create_table :achieved_badges do |t|
      t.references :user, foreign_key: true
      t.references :goal, foreign_key: true
      t.boolean :approved, default: false
      t.integer :level
      t.integer :money
      t.date :received_at
    end
  end
end
