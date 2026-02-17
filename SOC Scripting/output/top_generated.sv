// AUTO-GENERATED FILE

module top;

logic clk;
logic rst_n;
logic u_cpu__irq;
logic [31:0] u_cpu__data_out;
logic [31:0] u_dma__data_in;
logic u_dma__done;
logic [31:0] u_mem__wr_data;
logic u_mem__ready;
logic u_uart__irq;
logic u_timer__irq;


// Instance: u_cpu
cpu_core u_cpu (
.clk(clk),
.rst_n(rst_n),
.irq(u_cpu__irq),
.data_out(u_cpu__data_out)

);

// Instance: u_dma
dma_engine u_dma (
.clk(clk),
.rst_n(rst_n),
.data_in(u_dma__data_in),
.done(u_dma__done)

);

// Instance: u_mem
memory_ctrl u_mem (
.clk(clk),
.rst_n(rst_n),
.wr_data(u_mem__wr_data),
.ready(u_mem__ready)

);

// Instance: u_uart
uart u_uart (
.clk(clk),
.rst_n(rst_n),
.irq(u_uart__irq)

);

// Instance: u_timer
timer u_timer (
.clk(clk),
.rst_n(rst_n),
.irq(u_timer__irq)

);

endmodule