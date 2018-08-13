ActiveAdmin.register Exercise do

  permit_params :description, :due_at, :level, :money,
    questions_attributes: [:id, :description, :answer_type, :_destroy]

  form do |f|
    f.inputs 'Exercise info' do
      f.input :description
      f.input :due_at, as: :datepicker, min_date: Date.today
    end
    f.inputs 'Goal info' do

      f.input :level, collection: Goal::LEVELS
      f.input :money
    end
    f.inputs 'Questions' do
      f.has_many :questions, heading: 'Questions', allow_destroy: true,
          new_record: true do |a|
        answer_types = [
          ['Upload', Question::ANSWER_TYPE_UPLOAD],
          ['Text', Question::ANSWER_TYPE_TEXT]
        ]
        a.input :answer_type, as: :select, collection: answer_types
        a.input :description
      end
    end
    f.actions
  end
end
