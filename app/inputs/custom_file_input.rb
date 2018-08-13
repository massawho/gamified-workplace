class CustomFileInput < SimpleForm::Inputs::FileInput
  def input(wrapper_options = nil)
    # :preview_version is a custom attribute from :input_html hash, so you can pick custom sizes
    version = input_html_options.delete(:preview_version)
    out = ActiveSupport::SafeBuffer.new # the output buffer we're going to build
    # allow multiple submissions without losing the tmp version
    out << @builder.hidden_field("#{attribute_name}_cache").html_safe
    # check if there's an uploaded file (eg: edit mode or form not saved)
    # append file input. it will work accordingly with your simple_form wrappers
    out << @builder.file_field(attribute_name, input_html_options)

    file = object.send("#{attribute_name}")

    if file.try(:present?)
      # append preview image to output
      out << "<div><small class=\"text-info\">Current uploaded file #{file.filename}</small></div>".html_safe
    end

    out
  end
end
