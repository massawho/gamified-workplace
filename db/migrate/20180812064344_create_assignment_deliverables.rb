class CreateAssignmentDeliverables < ActiveRecord::Migration[5.2]
  def change
    create_table :assignment_deliverables do |t|
      t.references :exercise, foreign_key: true
      t.references :user, foreign_key: true

      t.timestamps
    end
  end
end
