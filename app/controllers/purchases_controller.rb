class PurchasesController < BaseController

  def create
    @product = Product.find params[:product_id]

    if @product.price > current_user.money
      return redirect_to :root, alert: 'Not enough points'
    end

    if !@product.can_purchase?(current_user)
      return redirect_to :root, alert: 'You have reached the limit for this product.'
    end

    if !@product.stock_available?
      return redirect_to :root, alert: 'No stock available for this product.'
    end

    purchase = Purchase.new
    purchase.product = @product
    purchase.user = current_user

    ApplicationRecord.transaction do
      purchase.save!

      current_user.money -= @product.price
      current_user.save!

      @product.decrease_stock
      @product.save!
    end

    redirect_to :root, notice: "Congratulations! You obtained #{product.name}"
  end
end
