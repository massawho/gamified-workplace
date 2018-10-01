ActiveAdmin.register AssignmentDeliverable do
  permit_params :correction_completed,
    answers_attributes: [:id, :feedback]

  index do
    selectable_column
    id_column
    column :exercise do |model|
      model.exercise.to_s
    end
    column :user do |model|
      model.user.name
    end
    column :username do |model|
      model.user.username
    end
    actions
  end

  form do |f|
    f.inputs 'Answers' do
      f.has_many :answers, heading: 'Answers', allow_destroy: false,
          new_record: false do |a|
        a.input :description, input_html: { readonly: true }
        a.input :feedback, as: :text
      end
    end

    f.inputs do
      f.input :correction_completed
    end

    f.actions
  end

end
