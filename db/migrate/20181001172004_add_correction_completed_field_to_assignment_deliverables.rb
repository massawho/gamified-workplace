class AddCorrectionCompletedFieldToAssignmentDeliverables < ActiveRecord::Migration[5.2]
  def change
    add_column :assignment_deliverables, :correction_completed, :boolean, default: false
  end
end
