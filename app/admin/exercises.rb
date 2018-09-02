ActiveAdmin.register Exercise do

  permit_params :description, :due_at, :level, :money,
    questions_attributes: [:id, :description, :answer_type, :file_name, :_destroy]

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
        a.input :file_name
        a.input :description
      end
    end
    f.actions
  end

  index do
    selectable_column
    column :description do |exercise|
      link_to exercise.description, admin_exercise_path(exercise)
    end
    column :due_at
    column :goal
    column :created_at
    column :updated_at
    actions defaults: true do |exercise|
      item "Download", download_admin_exercise_path(exercise), class: "member_link"
    end
  end

  member_action :download, method: :get do
    es = Exercise::DownloadService.new
    send_file es.create_downloadable_file(Exercise.find(params[:id]))
  end
end
