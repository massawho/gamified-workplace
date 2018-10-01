class AssignmentDeliverablesController < BaseController

  def create
    create_or_find_assignment
    redirect_to edit_assignment_deliverable_path(id: @record.id)
  end

  def edit
    @record = AssignmentDeliverable.find_by! id: params[:id]
    authorize! :update, @record
  end

  def update
    @record = AssignmentDeliverable.find_by! id: params[:id]
    authorize! :update, @record

    if @record.update assignment_deliverable_params
      flash[:success] = 'Assignment saved successfuly.'
      redirect_to :root
    else
      render :edit
    end

  end

  def show
    @record = AssignmentDeliverable.find_by! id: params[:id]
    authorize! :show, @record
  end

  def create_or_find_assignment

    @exercise = Exercise.find_by! id: params[:exercise_id]
    @record = AssignmentDeliverable.find_by exercise: @exercise, user: current_user

    return unless @record.nil?

    @record = AssignmentDeliverable.new
    @exercise.questions.each do |question|
      @record.answers << question.generate_answer
    end

    @record.exercise = @exercise
    @record.user = current_user

    @record.save
  end

  private

  def assignment_deliverable_params
    params.require(:assignment_deliverable).permit(answers_attributes: [:id, :upload, :extensive_answer])
  end
end
