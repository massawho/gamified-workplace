ActiveAdmin.register Goal do

  permit_params :description, :money, :frequency, :starts_at, :ends_at, :level, :is_active,
    achieved_badges_attributes: [:id, :user_id, :approved, :received_at, :_destroy]

  form do |f|
    frequencies = [
      ['Once', Goal::ONCE],
      ['Daily', Goal::DAILY],
      ['Weekly', Goal::WEEKLY],
      ['Biweekly', Goal::BIWEEKLY],
      ['Monthly', Goal::MONTHLY]
    ]


    f.inputs do
      f.input :description
      f.input :money
      f.input :frequency, as: :select, collection: frequencies
      f.input :starts_at, as: :datepicker, min_date: Date.today
      f.input :ends_at, as: :datepicker, min_date: Date.today
      f.input :level, as: :select, collection: Goal::LEVELS
      f.input :is_active, as: :boolean
    end

    f.inputs 'Achieved badges' do
      f.has_many :achieved_badges, heading: 'Badge', new_record: true do |a|
        a.input :received_at, as: :datepicker
        a.input :approved
        a.input :user, collection: User.all.map {|u| ["#{u.username}, #{u.name}", u.id]}
      end
    end

    f.actions
  end
end
