class CreateProducts < ActiveRecord::Migration[5.2]
  def change
    create_table :products do |t|
      t.string :name
      t.integer :price
      t.string :description
      t.integer :stock
      t.integer :max_per_user
      t.boolean :is_active
      t.boolean :is_featured
      t.string :photo

      t.timestamps
    end
  end
end
