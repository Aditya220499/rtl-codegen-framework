// AUTO-GENERATED FILE

module top;

logic irq;
logic [31:0] data_out;


// Instance: u_cpu
cpu u_cpu (
.irq(irq),
.data_out(data_out)

);

// Instance: u_uart
uart u_uart (
.irq(irq)

);

// Instance: u_dma
dma u_dma (
.data_out(data_out)

);

endmodule