def identify_spikes(prices, sma_period=12, backwards_threshold=3, forwards_threshold=2):
    # Calculate moving average
    sma = calculate_sma(prices, sma_period)
    
    spikes = []
    for i in range(len(prices) - sma_period + 1):
        current_price = prices[i + sma_period - 1]
        current_sma = sma[i]
        
        # Backward spike detection (price is 3x the moving average)
        if current_price > (current_sma * backwards_threshold):
            spikes.append({
                'index': i + sma_period - 1,
                'price': current_price,
                'sma': current_sma,
                'type': 'backward',
                'ratio': current_price / current_sma
            })
    
    # Forward spike detection using future average
    for i in range(len(prices) - sma_period):
        current_price = prices[i]
        future_window = prices[i+1:i+sma_period+1]
        future_avg = sum(future_window) / len(future_window)
        
        # Price is 2x the future average and at least 15 units higher
        if current_price > (future_avg * forwards_threshold) and current_price > (future_avg + 15):
            spikes.append({
                'index': i,
                'price': current_price,
                'future_avg': future_avg,
                'type': 'forward',
                'ratio': current_price / future_avg
            })
    
    return spikes

# Example usage:
spikes = identify_spikes(prices)
for spike in spikes:
    if spike['type'] == 'backward':
        print(f"Backward spike at index {spike['index']}: Price {spike['price']:.2f} is {spike['ratio']:.2f}x the SMA {spike['sma']:.2f}")
    else:
        print(f"Forward spike at index {spike['index']}: Price {spike['price']:.2f} is {spike['ratio']:.2f}x the future average {spike['future_avg']:.2f}")